"""Tests for release isolation, complete local projection and verified install archives."""
from __future__ import annotations

import copy
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

import build_editions as builder


class EditionBuildTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="director-edition-test-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.source = self.base / "source" / builder.PACKAGE
        self.output = self.base / "releases"
        self.source.mkdir(parents=True)
        self.files = {
            "SKILL.md": (
                "---\nname: director-seedance-prompt\ndescription: Compile video prompts.\n---\n"
                "# Director\n\nChoose 飞书 collaboration or local work.\n\n"
                "[Workspace](knowledge/02H_FEISHU_ASSET_WORKSPACE.md)\n\n"
                "[Image](knowledge/02G_IMAGE_CAPABILITY_FALLBACK.md)\n"
                "[Writer](knowledge/01A_SCREENWRITER_HANDOFF.md)\n"
            ).encode(),
            "knowledge/02H_FEISHU_ASSET_WORKSPACE.md": "飞书资产接口\n".encode(),
            "knowledge/02G_IMAGE_CAPABILITY_FALLBACK.md":
                "Use the user's authorized OpenAI image API, or confirmed text-only mode.\n".encode(),
            "knowledge/01A_SCREENWRITER_HANDOFF.md":
                "[Writer](../../viral-screenwriter/SKILL.md)\n".encode(),
            "knowledge/05_ACTION_PERFORMANCE_BODY_MECHANICS.md":
                "演员原台词、动态空间、角色身份、镜头连续性与表情余态保持。\n".encode(),
            "LICENSE": b"Private owner license; retain this file.\n",
            ".gitignore": b"__pycache__/\n",
            "README.md": b"Source-only overview.\n",
            "INSTALL.md": b"Source-only install guidance.\n",
            builder.README_TEMPLATE:
                "# @@EDITION_LABEL@@\n@@VERSION@@\n@@EDITION_DETAIL@@\n[Skill](SKILL.md)\n".encode(),
            builder.INSTALL_TEMPLATE:
                "# @@EDITION_LABEL@@\n@@VERSION@@\n@@EDITION_DETAIL@@\n[License](LICENSE)\n".encode(),
        }
        self.config = {
            "schema_version": 1,
            "exclude_files": ["knowledge/02H_FEISHU_ASSET_WORKSPACE.md"],
            "patches": [
                {
                    "id": "workspace",
                    "path": "SKILL.md",
                    "before": "Choose 飞书 collaboration or local work.",
                    "after": "Use workspace_mode=local and the existing project folder.",
                },
                {
                    "id": "loading",
                    "path": "SKILL.md",
                    "before": "[Workspace](knowledge/02H_FEISHU_ASSET_WORKSPACE.md)",
                    "after": "",
                },
            ],
        }
        self.metadata = {
            "schema_version": 1,
            "package": builder.PACKAGE,
            "edition": "source-test",
            "path_base": "package-root",
            "optional_external_skills": ["viral-screenwriter"],
            "optional_runtime_integrations": [
                {"name": "feishu-base", "entry": "knowledge/02H_FEISHU_ASSET_WORKSPACE.md"}
            ],
            "embedded_capabilities": [],
        }
        self.flush()

    def flush(self) -> None:
        self.files[builder.CONFIG] = builder.json_bytes(self.config)
        for name, data in self.files.items():
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        manifest = copy.deepcopy(self.metadata)
        manifest["files"] = [
            {"path": name, "bytes": len(data), "sha256": builder.sha256(data)}
            for name, data in sorted(self.files.items())
        ]
        (self.source / "package-manifest.json").write_bytes(builder.json_bytes(manifest))

    def snapshot(self) -> dict[str, bytes]:
        return {path.relative_to(self.source).as_posix(): path.read_bytes()
                for path in self.source.rglob("*") if path.is_file()}

    def test_both_archives_import_and_verify_without_changing_source(self) -> None:
        before = self.snapshot()
        proof = builder.build(self.source, self.output, "2026-10-20-v5")
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(len(proof["editions"]), 2)
        for item in proof["editions"]:
            with self.subTest(edition=item["edition"]):
                archive = self.output / item["archive"]
                verified = builder.verify_archive(archive, item["edition"])
                self.assertTrue(verified["single_root_skill"])
                self.assertGreater(verified["local_links_verified"], 0)
                self.assertEqual(verified["optional_external_skill_links"], ["viral-screenwriter/SKILL.md"])
                self.assertEqual(builder.sha256(archive.read_bytes()), item["sha256"])
                sidecar = archive.with_name(archive.name + ".sha256").read_text(encoding="utf-8")
                self.assertEqual(sidecar.strip().split()[0], item["sha256"])
                with zipfile.ZipFile(archive) as data:
                    names = data.namelist()
                    self.assertFalse(any("/maintenance/" in name for name in names))
                    manifest = json.loads(data.read(f"{builder.PACKAGE}/package-manifest.json"))
                    self.assertEqual(manifest["edition"], item["edition"])
                    self.assertEqual(manifest["version"], "2026-10-20-v5")
                    self.assertEqual(data.read(f"{builder.PACKAGE}/LICENSE"), self.files["LICENSE"])
                    self.assertEqual(data.read(f"{builder.PACKAGE}/knowledge/02G_IMAGE_CAPABILITY_FALLBACK.md"),
                                     self.files["knowledge/02G_IMAGE_CAPABILITY_FALLBACK.md"])
                    if item["edition"] == "local":
                        self.assertNotIn(f"{builder.PACKAGE}/knowledge/02H_FEISHU_ASSET_WORKSPACE.md", names)
                        self.assertEqual(manifest["optional_runtime_integrations"], [])
                    else:
                        self.assertEqual(data.read(f"{builder.PACKAGE}/SKILL.md"), self.files["SKILL.md"])
                        self.assertEqual(len(manifest["optional_runtime_integrations"]), 1)
        self.assertTrue((self.output / f"{builder.PACKAGE}-2026-10-20-v5-build-proof.json").is_file())

    def test_undeclared_files_never_enter_packages(self) -> None:
        (self.source / "private-cookie.txt").write_text("must not ship", encoding="utf-8")
        (self.source / "unreviewed.md").write_text("undeclared", encoding="utf-8")
        proof = builder.build(self.source, self.output, "test")
        for item in proof["editions"]:
            with zipfile.ZipFile(self.output / item["archive"]) as archive:
                self.assertFalse(any("private-cookie" in name or "unreviewed" in name for name in archive.namelist()))

    def test_stale_source_hash_is_rejected_before_output(self) -> None:
        (self.source / "SKILL.md").write_bytes(self.files["SKILL.md"] + b"\nchanged")
        with self.assertRaisesRegex(builder.BuildError, "source hash/size"):
            builder.build(self.source, self.output, "test")
        self.assertFalse(self.output.exists())

    def test_manifest_cannot_include_secret_or_archive(self) -> None:
        for name in (".env", "credentials.json", "cache.zip", "node_modules/package.json",
                     ".git/config", "archive.dpapi"):
            with self.subTest(name=name):
                with self.assertRaises(builder.BuildError):
                    builder.permitted_source_path(name)

    def test_manifest_rejects_path_escape_and_platform_absolute_paths(self) -> None:
        for name in ("../outside.md", "/outside.md", "C:/outside.md", "a\\outside.md", "a/./file.md"):
            with self.subTest(name=name):
                with self.assertRaises(builder.BuildError):
                    builder.safe_relative(name)

    def test_output_cannot_be_source_or_source_child(self) -> None:
        for path in (self.source, self.source / "dist"):
            with self.subTest(path=str(path)):
                with self.assertRaisesRegex(builder.BuildError, "outside the source"):
                    builder.build(self.source, path, "test")
        self.assertFalse((self.source / "dist").exists())

    def test_missing_or_ambiguous_projection_stops_build(self) -> None:
        for before in ("renamed text with no match", "local"):
            with self.subTest(before=before):
                config = copy.deepcopy(self.config)
                config["patches"][0]["before"] = before
                files = dict(self.files)
                if before == "local":
                    files["SKILL.md"] += b"\nlocal\n"
                with self.assertRaisesRegex(builder.BuildError, "expected 1 match"):
                    builder.apply_local_projection(files, config)

    def test_new_cloud_instruction_requires_explicit_projection(self) -> None:
        self.files["knowledge/new-route.md"] = "资产也可以查找飞书多维表。\n".encode()
        self.flush()
        with self.assertRaisesRegex(builder.BuildError, "unprojected cloud route"):
            builder.build(self.source, self.output, "test")
        self.assertFalse(self.output.exists())

    def test_cloud_reference_cannot_hide_in_unlinked_runtime_script(self) -> None:
        self.files["scripts/new_helper.py"] = b"# Connect using feishu\n"
        self.flush()
        with self.assertRaisesRegex(builder.BuildError, "cloud route"):
            builder.build(self.source, self.output, "test")
        self.assertFalse(self.output.exists())

    def test_unremoved_cloud_filename_is_rejected(self) -> None:
        self.files["references/new-feishu-api.md"] = b"API note.\n"
        self.flush()
        with self.assertRaisesRegex(builder.BuildError, "cloud resource"):
            builder.build(self.source, self.output, "test")

    def test_authorized_image_api_is_preserved(self) -> None:
        projected, changes = builder.apply_local_projection(self.files, self.config)
        image = "knowledge/02G_IMAGE_CAPABILITY_FALLBACK.md"
        self.assertEqual(projected[image], self.files[image])
        self.assertNotIn(image, [change["path"] for change in changes])
        self.assertIn(b"authorized OpenAI image API", projected[image])

    def test_broken_local_link_prevents_publishing_both_editions(self) -> None:
        self.files["knowledge/broken.md"] = b"[Missing](does-not-exist.md)\n"
        self.flush()
        with self.assertRaisesRegex(builder.BuildError, "broken package link"):
            builder.build(self.source, self.output, "test")
        self.assertFalse(self.output.exists())

    def test_undeclared_external_skill_link_is_rejected(self) -> None:
        self.files["knowledge/external.md"] = b"[Other](../../another-skill/SKILL.md)\n"
        self.flush()
        with self.assertRaisesRegex(builder.BuildError, "undeclared external"):
            builder.build(self.source, self.output, "test")

    def test_broken_code_span_loading_route_is_rejected(self) -> None:
        self.files["SKILL.md"] += b"\n`knowledge/missing.md`\n"
        self.flush()
        with self.assertRaisesRegex(builder.BuildError, "broken entrypoint route"):
            builder.build(self.source, self.output, "test")

    def test_nested_skill_entrypoint_is_rejected(self) -> None:
        self.files["capabilities/other/SKILL.md"] = b"nested entry\n"
        self.flush()
        with self.assertRaisesRegex(builder.BuildError, "exactly one"):
            builder.build(self.source, self.output, "test")

    def test_version_and_existing_release_are_not_silently_overwritten(self) -> None:
        with self.assertRaisesRegex(builder.BuildError, "release identifier"):
            builder.build(self.source, self.output, "../bad")
        builder.build(self.source, self.output, "test")
        before = {path.name: path.read_bytes() for path in self.output.iterdir()}
        with self.assertRaisesRegex(builder.BuildError, "already exists"):
            builder.build(self.source, self.output, "test")
        self.assertEqual(before, {path.name: path.read_bytes() for path in self.output.iterdir()})

    def test_archive_output_is_reproducible(self) -> None:
        first = builder.build(self.source, self.output, "test")
        second = builder.build(self.source, self.base / "other-releases", "test")
        self.assertEqual([item["sha256"] for item in first["editions"]],
                         [item["sha256"] for item in second["editions"]])

    def test_archive_extraction_rejects_path_escape(self) -> None:
        bad = self.base / "bad.zip"
        with zipfile.ZipFile(bad, "w") as archive:
            archive.writestr("../outside.md", b"bad")
        with self.assertRaisesRegex(builder.BuildError, "unsafe package path"):
            builder.verify_archive(bad, "local")
        self.assertFalse((self.base / "outside.md").exists())

    def test_archive_manifest_hash_detects_changed_payload(self) -> None:
        proof = builder.build(self.source, self.output, "test")
        good = self.output / proof["editions"][0]["archive"]
        bad = self.base / "tampered.zip"
        with zipfile.ZipFile(good) as origin, zipfile.ZipFile(bad, "w") as changed:
            for member in origin.infolist():
                data = origin.read(member)
                if member.filename.endswith("/LICENSE"):
                    data += b"changed"
                changed.writestr(member, data)
        with self.assertRaisesRegex(builder.BuildError, "extracted hash/size mismatch"):
            builder.verify_archive(bad, "feishu")

    def test_current_real_projection_preserves_all_unrelated_runtime_bytes(self) -> None:
        """Protect the actual full skill, including image fallback, during projection maintenance."""
        source = Path(__file__).resolve().parents[1]
        manifest_path = source / "package-manifest.json"
        if not (source / builder.CONFIG).is_file() or not manifest_path.is_file():
            self.skipTest("source-only projection configuration is not included in install editions")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        # This is a transformation regression, independent of release-manifest regeneration.
        # The release command separately enforces every exact source hash.
        files = {item["path"]: (source / item["path"]).read_bytes() for item in manifest["files"]
                 if not builder.is_shared_excluded(item["path"])}
        config = json.loads((source / builder.CONFIG).read_text(encoding="utf-8"))
        projected, changes = builder.apply_local_projection(files, config)
        changed = {item["path"] for item in changes}
        for name, data in files.items():
            if name not in changed:
                self.assertEqual(projected[name], data, name)
        self.assertEqual(
            projected["knowledge/02G_IMAGE_CAPABILITY_FALLBACK.md"],
            files["knowledge/02G_IMAGE_CAPABILITY_FALLBACK.md"],
        )
        # Source README/INSTALL are replaced by edition templates in the real build.
        builder.check_local_runtime({name: data for name, data in projected.items()
                                     if name not in {"README.md", "INSTALL.md"}})
        local_handoff = projected["knowledge/01A_SCREENWRITER_HANDOFF.md"].decode("utf-8")
        self.assertIn("workspace_mode=local", local_handoff)
        self.assertIn("SHA256", local_handoff)
        self.assertIn("旧提示词/视频", local_handoff)
        local_expression = projected["knowledge/05E_EXPRESSION_CUES.md"].decode("utf-8")
        self.assertIn("母图精确资产ID/修订ID", local_expression)
        self.assertIn("已验收基线", local_expression)


class SourceManifestFreshnessTests(unittest.TestCase):
    """Source checkout only (this file is not shipped): catch a manifest that was not refreshed."""

    def test_manifest_and_index_match_the_working_tree(self) -> None:
        import contextlib
        import importlib.util
        import io

        script = Path(__file__).resolve().parents[1] / "maintenance" / "refresh_manifest.py"
        if not script.is_file():
            self.skipTest("maintenance/refresh_manifest.py is not present")
        spec = importlib.util.spec_from_file_location("refresh_manifest", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = module.main(["--check"])
        self.assertEqual(code, 0, "run `python -B maintenance/refresh_manifest.py` and commit the result:\n"
                         + buffer.getvalue())


if __name__ == "__main__":
    unittest.main()
