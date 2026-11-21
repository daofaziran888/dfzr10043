"""__NAME__领域服务：字段、状态和动作来自业务配置，数据处理骨架由基类复用。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class SchedulePlanService(BaseModuleService):
    MODULE = "schedule_plan"
    ENTITY = "排程计划"
    OPERATION_TERM = "关联"
    LIST_FIELDS = ["计划编号", "关联模板", "触发周期", "时区设定", "生效起日", "生效止日", "并发上限", "下次触发"]
    REQUIRED_FIELDS = ["计划编号", "关联模板", "触发周期"]
    STATUS_ORDER = ["待生效", "生效中", "已暂停", "已过期"]
    ACTION_RULES = {"启效排程": "生效中", "暂停排程": "已暂停", "终止排程": "已过期"}
    NEGATIVE_ACTIONS = []
