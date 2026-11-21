"""表单字段服务：取值绑定、校验规则和填充顺序管理。

维护流程中表单填充字段的取值来源、校验规则和填充顺序，
校验失败时阻断该步骤。支持重试校验和按模板筛选。
"""
from __future__ import annotations

from typing import Any

from app.services.base import BaseModuleService


class FormFieldService(BaseModuleService):
    MODULE = "form_field"
    ENTITY = "填充字段"
    OPERATION_TERM = "采集"
    LIST_FIELDS = [
        "字段编号", "关联模板", "表单名称", "字段名称", "取值来源",
        "校验规则", "填充顺序", "失败提示",
    ]
    REQUIRED_FIELDS = ["字段编号", "关联模板", "字段名称"]
    STATUS_ORDER = ["草稿", "已绑定", "校验失败", "已停用"]
    ACTION_RULES = {"绑定取值": "已绑定", "重新校验": "校验失败", "停用字段": "已停用"}
    NEGATIVE_ACTIONS = ["停用字段"]

    def validate_field(self, field_id: int, actual_value: str = "") -> dict[str, Any]:
        """校验表单字段：取值来源非空则通过，否则标记校验失败。"""
        entry = self.get_entry(field_id)
        if entry is None:
            return {"ok": False, "reason": "字段不存在"}
        source = entry.get("取值来源", "")
        if not source or str(source).strip() == str(entry.get("字段名称", "")):
            self.run_action(field_id, "重新校验")
            return {"ok": False, "reason": "取值来源无效，校验失败"}
        self.run_action(field_id, "绑定取值")
        return {"ok": True, "field_id": field_id, "valid": True}

    def get_fields_by_template(self, template_code: str) -> list[dict[str, Any]]:
        """按关联模板获取表单字段列表。"""
        items, _ = self.list_entries(size=10000)
        return [it for it in items if it.get("关联模板") == template_code]