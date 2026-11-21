"""元素定位服务：多重定位策略、漂移检测与校验管理。

维护网页元素的多重定位策略与漂移检测记录，保障流程在页面
结构变化后仍能命中目标元素。支持选择器类型切换和备选恢复。
"""
from __future__ import annotations

from typing import Any

from app.services.base import BaseModuleService


class ElementLocatorService(BaseModuleService):
    MODULE = "element_locator"
    ENTITY = "定位策略"
    OPERATION_TERM = "采集"
    LIST_FIELDS = [
        "定位编号", "所属模板", "元素名称", "选择器类型", "选择器表达式",
        "备选表达式", "命中次数", "最近校验",
    ]
    REQUIRED_FIELDS = ["定位编号", "所属模板", "元素名称"]
    STATUS_ORDER = ["待校验", "有效", "已漂移", "已弃用"]
    ACTION_RULES = {"发起校验": "有效", "标记漂移": "已漂移", "弃用定位": "已弃用"}
    NEGATIVE_ACTIONS = []

    def detect_drift(self, locator_id: int) -> dict[str, Any]:
        """检测元素定位是否漂移：命中次数归零则为漂移。"""
        entry = self.get_entry(locator_id)
        if entry is None:
            return {"ok": False, "reason": "定位策略不存在"}
        hits = int(entry.get("命中次数", "0") or "0")
        if hits <= 0:
            self.run_action(locator_id, "标记漂移")
            return {"ok": True, "locator_id": locator_id, "drifted": True}
        return {"ok": True, "locator_id": locator_id, "drifted": False, "hits": hits}

    def get_locators_by_template(self, template_code: str) -> list[dict[str, Any]]:
        """按所属模板获取定位策略列表。"""
        items, _ = self.list_entries(size=10000)
        return [it for it in items if it.get("所属模板") == template_code]

    def try_backup_selector(self, locator_id: int) -> dict[str, Any]:
        """漂移时尝试使用备选表达式恢复。"""
        entry = self.get_entry(locator_id)
        if entry is None:
            return {"ok": False, "reason": "定位策略不存在"}
        backup = entry.get("备选表达式", "")
        if not backup or backup == entry.get("选择器表达式", ""):
            return {"ok": False, "reason": "无可用备选表达式"}
        entry["选择器表达式"] = backup
        self.run_action(locator_id, "发起校验")
        return {"ok": True, "locator_id": locator_id, "recovered_with_backup": True}