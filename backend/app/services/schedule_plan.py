"""排程计划服务：周期性排程、时区管理与任务投递。

维护流程的周期性排程、时区设定和生效区间，触发时向任务
队列投递排队任务。支持迟到数据防护和并发上限控制。
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from app.services.base import BaseModuleService


class SchedulePlanService(BaseModuleService):
    MODULE = "schedule_plan"
    ENTITY = "排程计划"
    OPERATION_TERM = "关联"
    LIST_FIELDS = [
        "计划编号", "关联模板", "触发周期", "时区设定", "生效起日",
        "生效止日", "并发上限", "下次触发",
    ]
    REQUIRED_FIELDS = ["计划编号", "关联模板", "触发周期"]
    STATUS_ORDER = ["待生效", "生效中", "已暂停", "已过期"]
    ACTION_RULES = {"启效排程": "生效中", "暂停排程": "已暂停", "终止排程": "已过期"}
    NEGATIVE_ACTIONS = []

    def check_late_arrival(self, plan_id: int) -> dict[str, Any]:
        """检查排程是否发生迟到数据（生效止日已过）。"""
        entry = self.get_entry(plan_id)
        if entry is None:
            return {"ok": False, "reason": "排程计划不存在"}
        end_date = entry.get("生效止日", "")
        if not end_date:
            return {"ok": True, "late": False}
        now = datetime.now(timezone(timedelta(hours=8))).isoformat()[:10]
        if end_date < now:
            self.run_action(plan_id, "终止排程")
            return {"ok": True, "late": True, "reason": f"生效止日{end_date}已过期，迟到数据拒绝"}
        return {"ok": True, "late": False}

    def get_active_plans(self) -> list[dict[str, Any]]:
        """获取生效中的排程计划列表。"""
        items, _ = self.list_entries(size=10000)
        return [it for it in items if it.get("status") == "生效中"]