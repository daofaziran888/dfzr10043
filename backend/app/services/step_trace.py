"""步骤轨迹服务：执行步骤记录、快照对比与异常标记。

记录流程每一步的输入输出快照与耗时，为失败定位和数据回溯
提供逐步骤证据链。支持复核、异常标记和归档流转。
"""
from __future__ import annotations

from typing import Any

from app.services.base import BaseModuleService


class StepTraceService(BaseModuleService):
    MODULE = "step_trace"
    ENTITY = "步骤轨迹"
    OPERATION_TERM = "关联"
    LIST_FIELDS = [
        "轨迹编号", "关联执行", "步骤序号", "步骤名称", "输入快照",
        "输出快照", "耗时毫秒", "退出码",
    ]
    REQUIRED_FIELDS = ["轨迹编号", "关联执行", "步骤序号"]
    STATUS_ORDER = ["已记录", "待复核", "异常", "已归档"]
    ACTION_RULES = {"提交复核": "待复核", "标记异常": "异常", "归档轨迹": "已归档"}
    NEGATIVE_ACTIONS = []

    def mark_abnormal(self, trace_id: int, exit_code: int = 1) -> dict[str, Any]:
        """标记步骤异常并设置退出码。"""
        entry = self.get_entry(trace_id)
        if entry is None:
            return {"ok": False, "reason": "轨迹不存在"}
        entry["退出码"] = str(exit_code)
        self.run_action(trace_id, "标记异常")
        return {"ok": True, "trace_id": trace_id, "exit_code": exit_code}

    def get_traces_by_run(self, run_code: str) -> list[dict[str, Any]]:
        """按关联执行编号获取所有步骤轨迹。"""
        items, _ = self.list_entries(size=10000)
        return [it for it in items if it.get("关联执行") == run_code]

    def archive_completed_traces(self) -> dict[str, Any]:
        """归档所有已完成步骤的轨迹。"""
        items, _ = self.list_entries(size=10000)
        archived = 0
        for it in items:
            if it.get("status") in ("已记录", "待复核"):
                self.run_action(it["id"], "归档轨迹")
                archived += 1
        return {"ok": True, "archived_count": archived}