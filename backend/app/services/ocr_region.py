"""识别区域服务：OCR区域标定、识别引擎与置信度管理。

维护流程中图像识别区域的坐标范围、识别引擎和语言设定，
置信度偏低时触发复核。支持多引擎切换和平均置信度计算。
"""
from __future__ import annotations

from typing import Any

from app.services.base import BaseModuleService


class OcrRegionService(BaseModuleService):
    MODULE = "ocr_region"
    ENTITY = "识别区域"
    OPERATION_TERM = "采集"
    LIST_FIELDS = [
        "区域编号", "关联模板", "区域名称", "坐标范围", "识别引擎",
        "语言设定", "平均置信度", "最近识别",
    ]
    REQUIRED_FIELDS = ["区域编号", "关联模板", "区域名称"]
    STATUS_ORDER = ["待标定", "已标定", "置信偏低", "已停用"]
    ACTION_RULES = {"标定区域": "已标定", "标记低置信": "置信偏低", "停用区域": "已停用"}
    NEGATIVE_ACTIONS = ["停用区域"]

    def check_confidence(self, region_id: int, threshold: float = 0.75) -> dict[str, Any]:
        """检查识别区域置信度，低于阈值则标记置信偏低。"""
        entry = self.get_entry(region_id)
        if entry is None:
            return {"ok": False, "reason": "识别区域不存在"}
        conf = float(entry.get("平均置信度", "0") or "0")
        if conf < threshold:
            self.run_action(region_id, "标记低置信")
            return {"ok": True, "region_id": region_id, "low_confidence": True, "score": conf}
        return {"ok": True, "region_id": region_id, "low_confidence": False, "score": conf}

    def get_regions_by_template(self, template_code: str) -> list[dict[str, Any]]:
        """按关联模板获取识别区域列表。"""
        items, _ = self.list_entries(size=10000)
        return [it for it in items if it.get("关联模板") == template_code]