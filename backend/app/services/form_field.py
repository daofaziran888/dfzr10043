"""__NAME__领域服务：字段、状态和动作来自业务配置，数据处理骨架由基类复用。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class FormFieldService(BaseModuleService):
    MODULE = "form_field"
    ENTITY = "填充字段"
    OPERATION_TERM = "关联"
    LIST_FIELDS = ["字段编号", "关联模板", "表单名称", "字段名称", "取值来源", "校验规则", "填充顺序", "失败提示"]
    REQUIRED_FIELDS = ["字段编号", "关联模板", "表单名称"]
    STATUS_ORDER = ["草稿", "已绑定", "校验失败", "已停用"]
    ACTION_RULES = {"绑定取值": "已绑定", "重新校验": "校验失败", "停用字段": "已停用"}
    NEGATIVE_ACTIONS = ["停用字段"]
