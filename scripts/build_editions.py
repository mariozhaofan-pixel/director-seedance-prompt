"""Build verified Feishu and local-only distributions from one manifest-controlled source.

Python 3.10+, standard library only. Does not install, execute bundled scripts,
change source files, or contact a service. Run from any directory:

    python -B scripts/build_editions.py --source . --output-dir ../release --version 2026-10-20-v5

The output directory must be outside the source tree. Existing release artifacts
are never overwritten. The maintained local projection is exact-match and fails
closed when source passages change or a new cloud route has no projection.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import shutil
import stat
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit


PACKAGE = "director-seedance-prompt"
CONFIG = "maintenance/editions/local-overrides.json"
README_TEMPLATE = "maintenance/editions/package-readme.md.in"
INSTALL_TEMPLATE = "maintenance/editions/package-install.md.in"
LOCAL_SIGNATURE = "作者：MARIOZHAOFAN｜微信：MARIOZHAOFAN｜抖音：晚上睡不赵"
EDITION_DETAILS = {
    "feishu": (
        "飞书连接版",
        "首次选择本地工作或飞书协作，已有项目沿用已确定模式。选择协作时按"
        "[02H 工作区](knowledge/02H_FEISHU_ASSET_WORKSPACE.md)配置连接及授权，"
        "在同一多维表中管理剧本、资产和段落，本地完成实际制作后增量同步。"
        "首次部署、授权和下载会增加启动时间；复用已有连接，依赖按需独立安装。"
        "本包不包含第三方 CLI、官方飞书 Skill、凭据或真实项目数据。"
        "同步规划器需要 Python 3.11+；实际读写成功以真实上传、读回及附件核验为准。",
    ),
    "local": (
        "独立版",
        "直接在本地项目文件夹工作。沿用用户已有目录，维护总索引、剧本修订、"
        "资产图、生图提示词、视频段落提示词和制作台账；先查看已有资产再补缺。"
        "编剧交接沿用同一本地项目与明确采用的稿件修订，用户视频保留原位。"
        "本版无需设置远程资产工作区，首次使用直接进入当前任务。\n\n" + LOCAL_SIGNATURE,
    ),
}
SHARED_EXCLUDES = {
    ".gitattributes", ".gitignore",
    "scripts/build_editions.py", "scripts/test_build_editions.py",
}
FORBIDDEN_PARTS = {
    ".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".venv", "venv",
    "node_modules", "credentials", "secrets", "backups", "archives",
    "adapters", "companion-skills", "packages",
}
FORBIDDEN_SUFFIXES = {
    ".zip", ".7z", ".rar", ".tar", ".gz", ".pyc", ".pyo", ".pem", ".key",
    ".dpapi", ".sqlite", ".db",
}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".py"}
CLOUD_ROUTE = re.compile(
    r"飞书|多维表|云表|云端|feishu|\blark(?:suite|-cli)?\b|"
    r"02H_FEISHU|同一?Base|共享剧本同步|sync-state\.json|pending-sync\.json|"
    r"分享密码|表字段映射|OAuth凭据",
    re.IGNORECASE,
)
MARKDOWN_LINK = re.compile(r"\[[^\]\n]+\]\(([^)\n]+)\)")
RUNTIME_PATH = re.compile(
    r"(?:knowledge|capabilities|references|examples|scripts)/[A-Za-z0-9_./-]+\.(?:md|py|json)"
)


class BuildError(ValueError):
    """A source or distribution failed a required invariant."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise BuildError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def safe_relative(value: str) -> str:
    require(isinstance(value, str) and bool(value), "empty package path")
    path = PurePosixPath(value)
    require(
        "\\" not in value and not path.is_absolute()
        and ":" not in value and all(part not in {"", ".", ".."} for part in value.split("/")),
        f"unsafe package path: {value}",
    )
    require(path.as_posix() == value, f"non-canonical package path: {value}")
    return value


def permitted_source_path(name: str) -> None:
    parts = PurePosixPath(name).parts
    require(not any(part.casefold() in FORBIDDEN_PARTS for part in parts),
            f"excluded directory in source manifest: {name}")
    require(PurePosixPath(name).suffix.casefold() not in FORBIDDEN_SUFFIXES,
            f"archive, credential or cache file in source manifest: {name}")
    basename = parts[-1].casefold()
    require(not (basename == ".env" or basename.startswith(".env.")
                 or re.search(r"(?:credentials?|cookies?|access[_-]?token|refresh[_-]?token)"
                              r"\.(?:json|txt|yaml|yml)$", basename)),
            f"private runtime data in source manifest: {name}")


def is_shared_excluded(name: str) -> bool:
    return name in SHARED_EXCLUDES or name.startswith("maintenance/")


def read_source(source: Path) -> tuple[dict, dict[str, bytes]]:
    manifest_path = source / "package-manifest.json"
    require(manifest_path.is_file() and not manifest_path.is_symlink(),
            "source package-manifest.json is missing or a symlink")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    require(manifest.get("package") == PACKAGE, "unexpected source package")
    require(manifest.get("path_base") == "package-root", "source manifest must use package-root paths")
    require(isinstance(manifest.get("files"), list), "source files must be a manifest array")
    files: dict[str, bytes] = {}
    case_paths: set[str] = set()
    for entry in manifest["files"]:
        name = safe_relative(entry["path"])
        require(name != "package-manifest.json", "manifest must not hash itself")
        require(name.casefold() not in case_paths, f"duplicate or case-colliding source path: {name}")
        permitted_source_path(name)
        path = source / name
        require(path.resolve().is_relative_to(source), f"source path escapes root: {name}")
        # Reject links anywhere along the declared file path, including junctions.
        for candidate in [path, *path.parents]:
            if candidate == source:
                break
            require(not candidate.is_symlink()
                    and not (hasattr(candidate, "is_junction") and candidate.is_junction()),
                    f"linked source path: {name}")
        require(path.is_file(), f"missing manifest file: {name}")
        data = path.read_bytes()
        require(len(data) == entry.get("bytes") and sha256(data) == entry.get("sha256"),
                f"source hash/size differs from manifest; refresh reviewed source manifest: {name}")
        files[name] = data
        case_paths.add(name.casefold())
    for needed in ("SKILL.md", CONFIG, README_TEMPLATE, INSTALL_TEMPLATE):
        require(needed in files, f"required source file not declared: {needed}")
    return manifest, files


def apply_local_projection(files: dict[str, bytes], config: dict) -> tuple[dict[str, bytes], list[dict]]:
    require(config.get("schema_version") == 1, "unsupported local projection schema")
    result = dict(files)
    changes: list[dict] = []
    excluded = config.get("exclude_files")
    patches = config.get("patches")
    require(isinstance(excluded, list) and isinstance(patches, list), "invalid local projection config")
    require(len(excluded) == len(set(excluded)), "duplicate local exclusion")
    for name in excluded:
        safe_relative(name)
        require(name in result, f"required local exclusion missing from source: {name}")
        del result[name]
        changes.append({"path": name, "operation": "exclude"})
    for patch in patches:
        name = safe_relative(patch["path"])
        require(name in result and name.endswith(".md"), f"invalid projection target: {name}")
        before, after = patch["before"], patch["after"]
        require(isinstance(before, str) and before and isinstance(after, str), f"invalid patch in {name}")
        old_bytes = result[name]
        # Matching ignores newline conventions; untouched files retain exact source bytes.
        text = old_bytes.decode("utf-8-sig").replace("\r\n", "\n")
        count = text.count(before)
        require(count == 1, f"local projection {patch.get('id', name)} expected 1 match, got {count}")
        result[name] = text.replace(before, after, 1).encode("utf-8")
        changes.append({
            "path": name, "operation": "replace", "patch": patch.get("id", name),
            "before_sha256": sha256(old_bytes), "after_sha256": sha256(result[name]),
        })
    return result, changes


def render_template(template: bytes, version: str, edition: str) -> bytes:
    label, detail = EDITION_DETAILS[edition]
    text = template.decode("utf-8-sig").replace("\r\n", "\n")
    for key, value in (("@@VERSION@@", version), ("@@EDITION_LABEL@@", label), ("@@EDITION_DETAIL@@", detail)):
        require(text.count(key) == 1, f"template must include {key} exactly once")
        text = text.replace(key, value)
    require(not re.search(r"@@[A-Z_]+@@", text), "unresolved package template placeholder")
    return text.encode("utf-8")


def check_local_runtime(files: dict[str, bytes]) -> None:
    for name, data in files.items():
        require(not CLOUD_ROUTE.search(name), f"cloud resource shipped in local edition: {name}")
        if PurePosixPath(name).suffix.casefold() in TEXT_SUFFIXES:
            found = CLOUD_ROUTE.search(data.decode("utf-8-sig"))
            require(found is None, f"unprojected cloud route in local edition: {name}: "
                    f"{found.group(0) if found else ''}")


def make_edition(source_manifest: dict, source_files: dict[str, bytes],
                 edition: str, version: str) -> tuple[dict[str, bytes], dict]:
    require(edition in EDITION_DETAILS, f"unknown edition: {edition}")
    files = {name: data for name, data in source_files.items() if not is_shared_excluded(name)}
    changes: list[dict] = []
    if edition == "local":
        config = json.loads(source_files[CONFIG].decode("utf-8-sig"))
        files, changes = apply_local_projection(files, config)
    files["README.md"] = render_template(source_files[README_TEMPLATE], version, edition)
    files["INSTALL.md"] = render_template(source_files[INSTALL_TEMPLATE], version, edition)
    require([name for name in files if PurePosixPath(name).name.casefold() == "skill.md"] == ["SKILL.md"],
            "an edition must contain exactly one root SKILL.md")
    if edition == "local":
        check_local_runtime(files)
    metadata = {key: copy.deepcopy(value) for key, value in source_manifest.items()
                if key not in {"files", "edition", "version", "source_edition", "build"}}
    metadata["version"] = version
    metadata["edition"] = edition
    metadata["source_edition"] = source_manifest.get("edition")
    metadata["build"] = {
        "source_manifest_controlled": True,
        "projection": "local-only" if edition == "local" else "source-runtime",
        "local_projection_sha256": sha256(source_files[CONFIG]) if edition == "local" else None,
    }
    if edition == "local":
        metadata["optional_runtime_integrations"] = []
    metadata["files"] = [
        {"path": name, "bytes": len(data), "sha256": sha256(data)}
        for name, data in sorted(files.items())
    ]
    files["package-manifest.json"] = json_bytes(metadata)
    return files, {
        "edition": edition, "files": len(files), "projection_changes": changes,
        "shared_excluded": sorted(name for name in source_files if is_shared_excluded(name)),
    }


def verify_directory(root: Path, edition: str) -> dict:
    manifest = json.loads((root / "package-manifest.json").read_text(encoding="utf-8"))
    require(manifest.get("package") == PACKAGE and manifest.get("edition") == edition,
            "extracted manifest identity mismatch")
    expected: dict[str, bytes] = {}
    expected_case: set[str] = set()
    for item in manifest["files"]:
        name = safe_relative(item["path"])
        permitted_source_path(name)
        require(name.casefold() not in expected_case, f"duplicate extracted manifest path: {name}")
        data = (root / name).read_bytes()
        require(len(data) == item["bytes"] and sha256(data) == item["sha256"],
                f"extracted hash/size mismatch: {name}")
        expected[name] = data
        expected_case.add(name.casefold())
    actual = {file.relative_to(root).as_posix() for file in root.rglob("*") if file.is_file()}
    require(actual == set(expected) | {"package-manifest.json"}, "archive inventory differs from manifest")
    require({name for name in actual if PurePosixPath(name).name.casefold() == "skill.md"} == {"SKILL.md"},
            "extracted edition must have exactly one SKILL.md")
    entry = expected["SKILL.md"].decode("utf-8-sig").replace("\r\n", "\n")
    require(re.match(r"\A---\n.*?^name:\s*director-seedance-prompt\s*$.*?\n---",
                     entry, re.DOTALL | re.MULTILINE) is not None, "skill name/frontmatter mismatch")
    local_links = 0
    external_links: set[str] = set()
    for name, data in expected.items():
        if not name.endswith(".md"):
            continue
        source = root / name
        for raw in MARKDOWN_LINK.findall(data.decode("utf-8-sig")):
            destination = raw.strip().strip("<>")
            if destination.startswith("#") or urlsplit(destination).scheme:
                continue
            relative = unquote(destination.split("#", 1)[0])
            if not relative:
                continue
            target = (source.parent / relative).resolve()
            if target.is_relative_to(root):
                require(target.exists(), f"broken package link: {name} -> {relative}")
                local_links += 1
            else:
                require(target == root.parent / "viral-screenwriter" / "SKILL.md"
                        and "viral-screenwriter" in manifest.get("optional_external_skills", []),
                        f"undeclared external package link: {name} -> {relative}")
                external_links.add("viral-screenwriter/SKILL.md")
    # The routing table uses code spans rather than Markdown links.
    for relative in set(RUNTIME_PATH.findall(entry)):
        require((root / relative).is_file(), f"broken entrypoint route: {relative}")
    for embedded in manifest.get("embedded_capabilities", []):
        require(embedded["entry"] in expected, f"missing embedded capability: {embedded['entry']}")
    for integration in manifest.get("optional_runtime_integrations", []):
        require(integration["entry"] in expected, f"missing integration: {integration['entry']}")
    if edition == "local":
        require(not manifest.get("optional_runtime_integrations"), "local edition advertises cloud integration")
        check_local_runtime(expected)
    return {
        "manifest_hashes_verified": len(expected), "local_links_verified": local_links,
        "optional_external_skill_links": sorted(external_links), "single_root_skill": True,
        "local_cloud_route_audit": "passed" if edition == "local" else "not_applicable",
    }


def write_zip(destination: Path, files: dict[str, bytes]) -> None:
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(f"{PACKAGE}/{name}", date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def verify_archive(archive_path: Path, edition: str) -> dict:
    """Validate CRC and safe inventory, then extract to a disposable isolated directory."""
    with tempfile.TemporaryDirectory(prefix="director-edition-verify-") as temporary:
        extraction = Path(temporary).resolve()
        with zipfile.ZipFile(archive_path) as archive:
            require(archive.testzip() is None, "archive CRC check failed")
            members = archive.infolist()
            seen: set[str] = set()
            for member in members:
                name = safe_relative(member.filename)
                require(name.startswith(PACKAGE + "/") and not member.is_dir(), "unexpected archive root")
                require(name.casefold() not in seen, "duplicate archive member")
                require(stat.S_IFMT(member.external_attr >> 16) != stat.S_IFLNK, "archive contains a symlink")
                target = extraction / name
                require(target.resolve().is_relative_to(extraction), "archive path escapes extraction root")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.read(member))
                seen.add(name.casefold())
        return verify_directory(extraction / PACKAGE, edition)


def build(source: Path, output_dir: Path, version: str) -> dict:
    source, output_dir = source.resolve(), output_dir.resolve()
    require(source.is_dir(), "source directory is missing")
    require(not output_dir.is_relative_to(source), "output directory must be outside the source tree")
    require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}", version) is not None,
            "version must be an explicit simple release identifier")
    names = [f"{PACKAGE}-{version}-{edition}.zip" for edition in EDITION_DETAILS]
    proof_name = f"{PACKAGE}-{version}-build-proof.json"
    final_names = [*names, *(name + ".sha256" for name in names), proof_name]
    require(not output_dir.exists() or output_dir.is_dir(), "output path is not a directory")
    for name in final_names:
        require(not (output_dir / name).exists(), f"release artifact already exists: {name}")
    source_manifest, source_files = read_source(source)
    proof = {
        "package": PACKAGE, "version": version,
        "source_manifest_sha256": sha256((source / "package-manifest.json").read_bytes()),
        "source_files_verified": len(source_files), "source_modified": False,
        "bundled_code_executed": False, "editions": [],
    }
    # All transformations and validations finish before any release is published.
    with tempfile.TemporaryDirectory(prefix="director-edition-build-") as temporary:
        stage = Path(temporary)
        for edition, filename in zip(EDITION_DETAILS, names):
            files, result = make_edition(source_manifest, source_files, edition, version)
            archive_path = stage / filename
            write_zip(archive_path, files)
            result.update(verify_archive(archive_path, edition))
            result.update({"archive": filename, "bytes": archive_path.stat().st_size,
                           "sha256": sha256(archive_path.read_bytes())})
            (stage / (filename + ".sha256")).write_text(
                f"{result['sha256']}  {filename}\n", encoding="utf-8", newline="\n")
            proof["editions"].append(result)
        # Detect a parallel source edit rather than publishing a stale mixed snapshot.
        latest_manifest, latest_files = read_source(source)
        require(latest_files == source_files and latest_manifest == source_manifest,
                "source changed during build; retry after source is stable")
        (stage / proof_name).write_bytes(json_bytes(proof))
        output_dir.mkdir(parents=True, exist_ok=True)
        for name in final_names:
            # Exclusive create also protects against a concurrent release into the same directory.
            with (output_dir / name).open("xb") as destination, (stage / name).open("rb") as origin:
                shutil.copyfileobj(origin, destination)
    return proof


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()
    try:
        proof = build(args.source, args.output_dir, args.version)
    except (BuildError, OSError, ValueError, KeyError, zipfile.BadZipFile) as error:
        parser.exit(1, f"Build failed: {error}\n")
    print(json.dumps({
        "output_dir": str(args.output_dir.resolve()),
        "version": proof["version"],
        "editions": [{key: item[key] for key in ("edition", "archive", "bytes", "sha256")}
                     for item in proof["editions"]],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
