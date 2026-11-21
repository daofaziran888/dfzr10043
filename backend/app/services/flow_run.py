"""流程执行服务：实例生命周期、派发、中止与执行状态追踪。

记录每次流程实例的派发节点、执行进度和产出记录数，
串联步骤轨迹与采集批次。支持按模板和节点维度查询。
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from app.services.base import BaseModuleService


class FlowRunService(BaseModuleService):
    MODULE = "flow_run"
    ENTITY = "执行实例"
    OPERATION_TERM = "采集"
    LIST_FIELDS = [
        "执行编号", "关联模板", "执行节点", "触发方式", "开始时间",
        "结束时间", "步骤进度", "产出记录数",
    ]
    REQUIRED_FIELDS = ["执行编号", "关联模板", "执行节点"]
    STATUS_ORDER = ["排队中", "执行中", "已完成", "执行失败"]
    ACTION_RULES = {"派发执行": "执行中", "中止执行": "已完成", "标记失败": "执行失败"}
    NEGATIVE_ACTIONS = []

    def complete_run(self, run_id: int, record_count: int = 0) -> dict[str, Any]:
        """完成执行实例，设置产出记录数和结束时间。"""
        entry = self.get_entry(run_id)
        if entry is None:
            return {"ok": False, "reason": "执行实例不存在"}
        self.run_action(run_id, "中止执行")
        now = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
        entry["结束时间"] = now
        entry["产出记录数"] = str(record_count)
        return {"ok": True, "run_id": run_id, "record_count": record_count}

    def fail_run(self, run_id: int, reason: str = "") -> dict[str, Any]:
        """标记执行失败。"""
        entry = self.get_entry(run_id)
        if entry is None:
            return {"ok": False, "reason": "执行实例不存在"}
        self.run_action(run_id, "标记失败")
        return {"ok": True, "run_id": run_id, "reason": reason}

    def get_runs_by_template(self, template_code: str) -> list[dict[str, Any]]:
        """按模板编号获取关联的执行实例。"""
        items, _ = self.list_entries(size=10000)
        return [it for it in items if it.get("关联模板") == template_code]