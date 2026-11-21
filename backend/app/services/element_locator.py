"""__NAME__领域服务：字段、状态和动作来自业务配置，数据处理骨架由基类复用。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class ElementLocatorService(BaseModuleService):
    MODULE = "element_locator"
    ENTITY = "定位策略"
    OPERATION_TERM = "校验"
    LIST_FIELDS = ["定位编号", "所属模板", "元素名称", "选择器类型", "选择器表达式", "备选表达式", "命中次数", "最近校验"]
    REQUIRED_FIELDS = ["定位编号", "所属模板", "元素名称"]
    STATUS_ORDER = ["待校验", "有效", "已漂移", "已弃用"]
    ACTION_RULES = {"发起校验": "有效", "标记漂移": "已漂移", "弃用定位": "已弃用"}
    NEGATIVE_ACTIONS = []
