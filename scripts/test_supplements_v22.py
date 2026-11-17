"""v22 supplements: vehicle tracking azimuths, driver performance and review order."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8-sig")


class V22VehicleTests(unittest.TestCase):
    def test_tracking_azimuths_performance_and_review_order(self) -> None:
        module = read("knowledge/05G_VEHICLE_CINEMA.md")
        self.assertIn("同样是平行跟拍，方位不同", module)
        self.assertIn("**驾驶者表演**", module)
        self.assertIn("审片按这个顺序看：身份", module)
        # the review order leads into the existing bounded-repair rule
        section = module.split("## 八、车辆常见问题与修法", 1)[1]
        self.assertLess(section.index("审片按这个顺序看"), section.index("返修按入口的 micro/local 范围"))

    def test_camera_rows(self) -> None:
        camera = read("knowledge/04_CAMERA_LIGHT_COLOR_STYLE.md")
        self.assertIn("| RED V-Raptor [X] 8K VV |", camera)
        self.assertIn("| ARRI Alexa 35（Super 35，近距离动作） |", camera)


if __name__ == "__main__":
    unittest.main()
