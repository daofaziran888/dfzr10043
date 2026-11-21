"""资源额度服务：额度管理、抢占优先级与降级处理。

维护节点并发、代理出口和识别引擎等资源额度池，
按抢占优先级决定流程能否派发，耗尽时触发节点降级。
"""
from __future__ import annotations

from typing import Any

from app.services.base import BaseModuleService


class ResourcePoolService(BaseModuleService):
    MODULE = "resource_pool"
    ENTITY = "资源额度"
    OPERATION_TERM = "校验"
    LIST_FIELDS = [
        "额度编号", "资源类型", "总额度", "已占用", "预留额度",
        "释放策略", "抢占优先级", "最近调整",
    ]
    REQUIRED_FIELDS = ["额度编号", "资源类型", "总额度"]
    STATUS_ORDER = ["充足", "紧张", "耗尽", "已冻结"]
    ACTION_RULES = {"调整额度": "紧张", "冻结资源": "已冻结", "释放预留": "充足"}
    NEGATIVE_ACTIONS = []

    def check_exhaustion(self, resource_id: int) -> dict[str, Any]:
        """检查资源是否耗尽：已占用+预留额度 >= 总额度。"""
        entry = self.get_entry(resource_id)
        if entry is None:
            return {"ok": False, "reason": "资源不存在"}
        total = int(entry.get("总额度", "0") or "0")
        used = int(entry.get("已占用", "0") or "0")
        reserved = int(entry.get("预留额度", "0") or "0")
        if used + reserved >= total:
            entry["status"] = "耗尽"
            return {"ok": True, "exhausted": True, "total": total, "used": used, "reserved": reserved}
        return {"ok": True, "exhausted": False, "total": total, "used": used, "reserved": reserved}

    def allocate_resources(self, resource_id: int, amount: int) -> dict[str, Any]:
        """分配资源额度（已占用增加）。"""
        entry = self.get_entry(resource_id)
        if entry is None:
            return {"ok": False, "reason": "资源不存在"}
        total = int(entry.get("总额度", "0") or "0")
        used = int(entry.get("已占用", "0") or "0")
        if used + amount > total:
            return {"ok": False, "reason": "资源额度不足"}
        entry["已占用"] = str(used + amount)
        remaining = total - (used + amount)
        if remaining <= 0:
            entry["status"] = "耗尽"
        elif remaining < total * 0.2:
            entry["status"] = "紧张"
        return {"ok": True, "allocated": amount, "remaining": remaining}

    def get_priority_order(self) -> list[dict[str, Any]]:
        """按抢占优先级排序返回非冻结资源。"""
        items, _ = self.list_entries(size=10000)
        active = [it for it in items if it.get("status") != "已冻结"]
        active.sort(key=lambda r: int(r.get("抢占优先级", "0") or "0"), reverse=True)
        return active