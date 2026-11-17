"""Incident logging and retro report."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import log_incident
import retro_report


class RetroTests(unittest.TestCase):
    def test_log_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "项目层" / "事故日志.md"
            log_incident.main(["--log", str(log), "--segment", "第七集第08段 v1", "--quote", "石头巨人手变成静态的了",
                               "--symptom", "石掌画成定格横臂", "--layer", "skill缺规则",
                               "--fix", "写成一直往下伸，被挡住才停", "--verified", "有效（v2）",
                               "--date", "2026-10-23"])
            log_incident.main(["--log", str(log), "--segment", "第七集第07段 v1", "--quote", "小灰拍手干嘛",
                               "--symptom", "反应没有原因", "--layer", "剧本问题", "--verified", "有效（v2）",
                               "--date", "2026-10-23"])
            log_incident.main(["--log", str(log), "--segment", "第七集第10段", "--quote", "模型认东南西北吗",
                               "--symptom", "提示词写了世界方位", "--layer", "skill有规则没执行",
                               "--date", "2026-10-23"])
            cards = retro_report.parse(log.read_text(encoding="utf-8"))
            self.assertEqual(len(cards), 3)
            text = retro_report.report(cards)
            self.assertIn("共 3 条事故卡", text)
            self.assertIn("第七集第08段 v1", text.split("## 提升候选", 1)[1])
            self.assertNotIn("小灰拍手", text.split("## 提升候选", 1)[1].split("## 待验证", 1)[0])
            self.assertIn("第七集第10段", text.split("## 待验证", 1)[1])

    def test_table_format_log(self) -> None:
        log = "\n".join([
            "skill-version: director-seedance-prompt 2026-11-03-v19",
            "",
            "# 事故日志",
            "",
            "## 第一集",
            "",
            "| 日期 | 段号 | 用户原话 | 症状 | 根因层 | 改法 | 下次出片是否验证 |",
            "| --- | --- | --- | --- | --- | --- | --- |",
            "| 2026-11-04 | 第12段 v1 | 「开错门了」 | 人从屋里出来 | 编译取舍（同时挂了两张图） | 只挂一张 | 已验证：12 v2 用户验收 |",
            "| 2026-11-04 | 第01段 v2 | 平台报错 | 声线不足 2 秒 | 平台限制 | 补静音 | 待出片 |",
            "| 2026-11-04 | 第04段 | 「又失败了」 | 判为不合规 | 平台限制（内容审核） | 改写 | 仍不合规（见下一行） |",
            "| 2026-11-05 | 画布 | 「提前建好干嘛」 | 一次建了44个节点 | skill 有规则但没执行（02A 每批两段） | 删空节点 | 已验证（回读） |",
            "| 2026-11-05 | 第07段 | 「拍手干嘛」 | 反应没有原因 | 剧本问题 | 交编剧 | 有效（v2） |",
            "",
            "正文里的其他表格不算：",
            "",
            "| 对象 | 状态 |",
            "| --- | --- |",
            "| 面碗 | 两碗 |",
        ])
        cards = retro_report.parse(log)
        self.assertEqual(len(cards), 5)
        self.assertEqual(cards[0]["title"], "2026-11-04 第12段 v1")
        text = retro_report.report(cards)
        self.assertIn("共 5 条事故卡", text)
        self.assertIn("| 平台限制 | 2 |", text)
        self.assertIn("| skill有规则没执行 | 1 |", text)
        self.assertIn("| 编译取舍 | 1 | 复盘时请用户判断 |", text)
        candidates = text.split("## 提升候选", 1)[1].split("## 待验证", 1)[0]
        self.assertIn("第12段 v1", candidates)
        self.assertIn("画布", candidates)
        self.assertNotIn("第07段", candidates)  # script problems go to the screenwriter
        self.assertNotIn("第04段", candidates)
        self.assertIn("第01段 v2", text.split("## 待验证", 1)[1])

    def test_status_and_layer_normalization(self) -> None:
        self.assertEqual(retro_report.status_of("有效（v2）"), "有效")
        self.assertEqual(retro_report.status_of("已生成、用户验收（2026-11-04）"), "有效")
        self.assertEqual(retro_report.status_of("待验收"), "待验证")
        self.assertEqual(retro_report.status_of("无效"), "无效")
        self.assertEqual(retro_report.layer_of("模型限制（复杂手势）"), "模型能力限制")
        self.assertEqual(retro_report.layer_of("项目偏好＋资产一致性没核"), "项目偏好")
        self.assertEqual(retro_report.layer_of(""), "待定")


if __name__ == "__main__":
    unittest.main()
