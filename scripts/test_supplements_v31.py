"""v31 supplements: keeping spoken dialogue natural when it is compiled or written by the director."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


def fidelity_section() -> str:
    text = read("knowledge/06_TIMELINE_EDITING_SOUND.md")
    return text.split("### 台词编译保真（补充）", 1)[1].split("\n## ", 1)[0]


class V31DialogueFidelityTests(unittest.TestCase):
    def test_compiled_lines_keep_their_spoken_form(self) -> None:
        section = fidelity_section()
        for phrase in ("逐字保留它说出口的样子", "不把口语改成书面句", "不合并碎句", "引号里只放说出口的字",
                       "不叠情绪形容词", "不为显得自然主动添加", "不压缩台词", "换成同音常用字", "剧本和台账保留原字"):
            self.assertIn(phrase, section)
        self.assertIn("5.5字/秒", section)

    def test_director_written_lines_have_a_checklist(self) -> None:
        section = fidelity_section()
        for phrase in ("先定这句话的情境", "references/dialogue-naturalness.md", "只改命中的句子",
                       "情绪没有被直接报出来", "回答不必句句正面接", "称呼只在叫住、警告、翻脸时出现",
                       "遮住名字能分出是谁在说", "不矫枉过正", "标明暂定"):
            self.assertIn(phrase, section)
        self.assertEqual(sum(1 for n in range(1, 8) if f"\n{n}. " in section), 7)
        # The package may only link to the screenwriter's entry file, so the page is named, not linked.
        self.assertNotIn("](../../viral-screenwriter/references", section)

    def test_example_no_longer_models_the_pattern(self) -> None:
        timeline = read("knowledge/06_TIMELINE_EDITING_SOUND.md")
        self.assertNotIn("我不是来问你", timeline)
        self.assertIn("“账我昨晚对过了，”", timeline)
        self.assertIn("“少的那一笔，是你签的字。”", timeline)

    def test_fault_rows_and_handoff(self) -> None:
        qc = read("knowledge/08_MODEL_QC_REPAIR.md")
        for row in ("| 台词像念稿或书面腔 |", "| 台词被加速念或吞字 |", "| 多音字、生僻字或专名读错 |"):
            self.assertIn(row, qc)
        handoff = read("knowledge/01A_SCREENWRITER_HANDOFF.md")
        self.assertIn("台词自然化", handoff)
        self.assertIn("哪些句子锁定不动", handoff)


if __name__ == "__main__":
    unittest.main()
