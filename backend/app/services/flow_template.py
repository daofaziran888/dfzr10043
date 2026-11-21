"""流程模板服务：模板发布、步骤编排、参数声明和版本管理。

流程模板是机器人执行的唯一流程定义来源，发布后才能被排程计划引用。
提供模板校验、调试记录查询、步骤数量统计等业务方法。
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from app.services.base import BaseModuleService


class FlowTemplateService(BaseModuleService):
    MODULE = "flow_template"
    ENTITY = "流程模板"
    OPERATION_TERM = "采集"
    LIST_FIELDS = [
        "模板编号", "流程名称", "起始地址", "步骤数量", "参数列表",
        "适用站点", "模板版本", "最近调试",
    ]
    REQUIRED_FIELDS = ["模板编号", "流程名称", "起始地址"]
    STATUS_ORDER = ["草稿", "调试中", "已发布", "已下线"]
    ACTION_RULES = {"提交调试": "调试中", "发布模板": "已发布", "下线模板": "已下线"}
    NEGATIVE_ACTIONS = ["下线模板"]

    def validate_template_steps(self, template_id: int) -> dict[str, Any]:
        """校验模板步骤是否合法：步骤数量必须>0，参数列表不能为空。"""
        entry = self.get_entry(template_id)
        if entry is None:
            return {"valid": False, "reason": "模板不存在"}
        step_count = entry.get("步骤数量", 0)
        if isinstance(step_count, str):
            try:
                step_count = int(step_count)
            except (ValueError, TypeError):
                step_count = 0
        if step_count <= 0:
            return {"valid": False, "reason": "模板步骤数量必须大于0"}
        params = entry.get("参数列表", "")
        if not params or str(params).strip() == template_id:
            return {"valid": False, "reason": "模板参数列表不能为空"}
        return {"valid": True, "template_id": template_id, "steps": step_count}

    def get_published_templates(self) -> list[dict[str, Any]]:
        """获取所有已发布的流程模板，供排程计划引用。"""
        items, _ = self.list_entries(size=10000)
        return [it for it in items if it.get("status") == "已发布"]

    def record_debug_session(self, template_id: int) -> dict[str, Any]:
        """记录模板调试会话并更新最近调试时间。"""
        entry = self.get_entry(template_id)
        if entry is None:
            return {"ok": False, "reason": "模板不存在"}
        now = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
        entry["最近调试"] = now
        return {"ok": True, "template_id": template_id, "debug_time": now}