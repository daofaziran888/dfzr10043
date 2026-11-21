"""__NAME__领域服务：字段、状态和动作来自业务配置，数据处理骨架由基类复用。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class ExceptionRuleService(BaseModuleService):
    MODULE = "exception_rule"
    ENTITY = "处置规则"
    OPERATION_TERM = "校验"
    LIST_FIELDS = ["规则编号", "匹配特征", "判定条件", "处置动作", "适用范围", "生效优先级", "命中次数", "最近命中"]
    REQUIRED_FIELDS = ["规则编号", "匹配特征", "判定条件"]
    STATUS_ORDER = ["草稿", "已生效", "已抑制", "已废弃"]
    ACTION_RULES = {"启效规则": "已生效", "抑制规则": "已抑制", "废弃规则": "已废弃"}
    NEGATIVE_ACTIONS = []
