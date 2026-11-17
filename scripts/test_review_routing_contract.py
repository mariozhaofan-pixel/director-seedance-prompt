"""Native Skill entrypoint, knowledge routing, and runtime integrity checks."""
from __future__ import annotations

import re
import unittest
from decimal import Decimal
from pathlib import Path
from urllib.parse import unquote, urlsplit

from validate_prompt import validate_prompt


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_SKILLS = {"viral-screenwriter"}
LINK_RE = re.compile(r"\[[^\]\n]+\]\(([^)\n]+)\)")


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def local_links(text: str):
    """Return concrete Markdown file references, ignoring web URLs and anchors."""
    for destination in LINK_RE.findall(text):
        destination = destination.strip().strip("<>")
        if destination.startswith("#") or urlsplit(destination).scheme:
            continue
        path = unquote(destination.split("#", 1)[0])
        if path:
            yield path


class RepositoryStructureTests(unittest.TestCase):
    def test_skill_frontmatter_and_name(self) -> None:
        skill = read("SKILL.md")
        frontmatter = re.match(r"\A---\n(?P<body>.*?)\n---(?:\n|\Z)", skill, re.DOTALL)
        self.assertIsNotNone(frontmatter, "SKILL.md must start with YAML frontmatter")
        body = frontmatter.group("body")
        name = re.search(r"^name:\s*([^\s#]+)\s*$", body, re.MULTILINE)
        self.assertIsNotNone(name, "SKILL.md frontmatter must define name")
        self.assertEqual(name.group(1), ROOT.name)
        self.assertRegex(name.group(1), r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertRegex(body, r"(?m)^description:\s*\S")

    def test_entry_runtime_paths_are_concrete_existing_files(self) -> None:
        paths = set(re.findall(r"(?:knowledge|capabilities|examples|scripts)/[A-Za-z0-9_./-]+\.(?:md|py)", read("SKILL.md")))
        self.assertTrue(paths)
        for relative_path in paths:
            with self.subTest(path=relative_path):
                target = (ROOT / relative_path).resolve()
                self.assertTrue(target.is_relative_to(ROOT))
                self.assertTrue(target.is_file(), relative_path)
        runtime = {path for path in paths if path.startswith("knowledge/")}
        self.assertIn("knowledge/08_FAST_PREFLIGHT.md", runtime)
        self.assertIn("knowledge/styles/STYLE_ROUTER.md", runtime)

    def test_runtime_links_resolve_or_target_declared_external_skills(self) -> None:
        sources = [ROOT / "SKILL.md", *(ROOT / "knowledge").rglob("*.md"), *(ROOT / "capabilities").rglob("*.md")]
        for source in sources:
            for relative in local_links(source.read_text(encoding="utf-8-sig")):
                with self.subTest(source=str(source.relative_to(ROOT)), target=relative):
                    target = (source.parent / relative).resolve()
                    if target.is_relative_to(ROOT):
                        self.assertTrue(target.exists(), f"broken runtime link: {relative}")
                    else:
                        self.assertEqual(target.name, "SKILL.md")
                        self.assertIn(target.parent.name, EXTERNAL_SKILLS)

    def test_only_the_root_is_a_skill_entrypoint(self) -> None:
        # companion-skills/ holds separately packaged peers and never enters this Skill's archives.
        entries = {path.relative_to(ROOT).as_posix() for path in ROOT.rglob("SKILL.md")
                   if "companion-skills" not in path.relative_to(ROOT).parts}
        self.assertEqual(entries, {"SKILL.md"})

    def test_english_style_files_are_discoverable_from_the_router(self) -> None:
        directory = ROOT / "knowledge/styles"
        styles = {path.resolve() for path in directory.rglob("*.md") if path.name != "STYLE_ROUTER.md"}
        self.assertTrue(styles)
        router = directory / "STYLE_ROUTER.md"
        linked = {(router.parent / relative).resolve() for relative in local_links(router.read_text(encoding="utf-8-sig"))}
        self.assertTrue(styles.issubset(linked), "every library style needs a router link")
        for path in styles:
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertRegex(path.name, r"^[a-z]+(?:-[a-z]+)*\.md$")
                self.assertRegex(path.parent.name, r"^[a-z]+(?:-[a-z]+)*$")

    def test_optional_modules_have_direct_specialized_callers(self) -> None:
        routes = {
            "knowledge/05_ACTION_PERFORMANCE_BODY_MECHANICS.md": "05A_COMBAT_EXCHANGE_VARIANTS.md",
            "knowledge/05C_COMBAT_CHOREOGRAPHY.md": "05A_COMBAT_EXCHANGE_VARIANTS.md",
            "knowledge/07_STYLE_GENRE_FAMOUS_SCENE_COMPILER.md": "07A_PAINTING_HOMAGE_ROUTER.md",
        }
        for source, expected in routes.items():
            with self.subTest(source=source):
                targets = {Path(path).name for path in local_links(read(source))}
                self.assertIn(expected, targets)
                reference = read("knowledge/" + expected)
                self.assertTrue(reference.startswith("# "))
                self.assertNotRegex(reference, r"(?m)^name:\s*")

    def test_capability_dependencies_are_external_links(self) -> None:
        for source, skill in (("knowledge/01A_SCREENWRITER_HANDOFF.md", "viral-screenwriter"),):
            with self.subTest(source=source):
                source_path = ROOT / source
                targets = {(source_path.parent / path).resolve() for path in local_links(read(source))}
                expected = (ROOT.parent / skill / "SKILL.md").resolve()
                self.assertIn(expected, targets)
                self.assertFalse(expected.is_relative_to(ROOT))

    def test_embedded_capability_routes_are_self_contained(self) -> None:
        routes = {
            "knowledge/02F_HIGGSFIELD_ASSET_PREPRODUCTION.md": "capabilities/asset-preproduction/ASSET_PREPRODUCTION.md",
            "knowledge/02B_CHARACTER_BOARD.md": "capabilities/asset-preproduction/ASSET_PREPRODUCTION.md",
            "knowledge/styles/STYLE_ROUTER.md": "capabilities/reference-rule-extraction/REFERENCE_RULE_EXTRACTION.md",
        }
        for source, relative in routes.items():
            with self.subTest(source=source):
                entry = (ROOT / relative).resolve()
                targets = {((ROOT / source).parent / path).resolve() for path in local_links(read(source))}
                self.assertIn(entry, targets)
                pending, visited = [entry], set()
                while pending:
                    document = pending.pop()
                    if document in visited:
                        continue
                    visited.add(document)
                    self.assertTrue(document.is_file(), str(document))
                    self.assertTrue(document.is_relative_to(ROOT))
                    if document.suffix == ".md":
                        for path in local_links(document.read_text(encoding="utf-8-sig")):
                            dependency = (document.parent / path).resolve()
                            self.assertTrue(dependency.is_file(), f"missing dependency: {dependency}")
                            # The optional writer handoff is checked separately;
                            # traverse the complete built-in resource closure without installing peers.
                            if dependency.is_relative_to(ROOT / "capabilities"):
                                pending.append(dependency)
                self.assertGreater(len(visited), 1, "capability must include its referenced functional resources")

    def test_entry_and_fast_preflight_have_bounded_context_size(self) -> None:
        entry = read("SKILL.md")
        links = set(re.findall(r"(?:knowledge|capabilities|examples|references)/[\w./-]+[.](?:md|json)", entry))
        self.assertGreater(len(links), 10)
        for link in links:
            self.assertTrue((ROOT / link).is_file(), link)
        self.assertLessEqual(len(read("knowledge/08_FAST_PREFLIGHT.md")), 8000)

    def test_standard_example_passes_actual_general_timed_validation(self) -> None:
        example = read("examples/seedance_25_standard.md")
        report = validate_prompt(example, version="2.5", profile="general", timeline="timed", duration=Decimal("24"))
        self.assertEqual(report["verdict"], "PASS", report["errors"])
        self.assertIn("timeline_coverage_0_to_T", report["checked"])

if __name__ == "__main__":
    unittest.main()
