"""数据落库服务：写入过程记录、冲突行处理、落库水位推进。

记录采集批次到目标存储的写入过程、冲突行处理和落库水位，
作为下游消费的唯一入口。水位单调递增，支持增量消费。
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from app.services.base import BaseModuleService


class DataLandingService(BaseModuleService):
    MODULE = "data_landing"
    ENTITY = "落库记录"
    OPERATION_TERM = "采集"
    LIST_FIELDS = [
        "落库编号", "关联批次", "目标存储", "写入模式", "写入行数",
        "冲突行数", "落库水位", "完成时间",
    ]
    REQUIRED_FIELDS = ["落库编号", "关联批次", "目标存储"]
    STATUS_ORDER = ["待写入", "写入中", "已写入", "写入异常"]
    ACTION_RULES = {"启动写入": "写入中", "确认写入": "已写入", "标记异常": "写入异常"}
    NEGATIVE_ACTIONS = []

    def advance_watermark(self, landing_id: int, watermark: int) -> dict[str, Any]:
        """推进落库水位（仅当新水位大于当前水位时生效）。"""
        entry = self.get_entry(landing_id)
        if entry is None:
            return {"ok": False, "reason": "落库记录不存在"}
        current = int(entry.get("落库水位", "0") or "0")
        if watermark > current:
            entry["落库水位"] = str(watermark)
            return {"ok": True, "landing_id": landing_id, "new_watermark": watermark}
        return {"ok": False, "reason": f"新水位{watermark}不大于当前水位{current}"}

    def get_watermark(self, target_storage: str) -> int:
        """获取指定目标存储的当前最高水位。"""
        items, _ = self.list_entries(size=10000)
        max_wm = 0
        for it in items:
            if it.get("目标存储") == target_storage and it.get("status") == "已写入":
                wm = int(it.get("落库水位", "0") or "0")
                if wm > max_wm:
                    max_wm = wm
        return max_wm

    def handle_conflicts(self, landing_id: int, conflict_count: int) -> dict[str, Any]:
        """处理冲突行：冲突行数>0则标记写入异常，否则确认写入。"""
        entry = self.get_entry(landing_id)
        if entry is None:
            return {"ok": False, "reason": "落库记录不存在"}
        if conflict_count > 0:
            self.run_action(landing_id, "标记异常")
            return {
                "ok": True,
                "landing_id": landing_id,
                "conflicts": conflict_count,
                "handled_as": "异常标记",
            }
        self.run_action(landing_id, "确认写入")
        return {"ok": True, "landing_id": landing_id, "conflicts": 0, "handled_as": "已确认"}