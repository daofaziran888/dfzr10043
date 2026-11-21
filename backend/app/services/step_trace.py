"""__NAME__领域服务：字段、状态和动作来自业务配置，数据处理骨架由基类复用。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class StepTraceService(BaseModuleService):
    MODULE = "step_trace"
    ENTITY = "步骤轨迹"
    OPERATION_TERM = "关联"
    LIST_FIELDS = ["轨迹编号", "关联执行", "步骤序号", "步骤名称", "输入快照", "输出快照", "耗时毫秒", "退出码"]
    REQUIRED_FIELDS = ["轨迹编号", "关联执行", "步骤序号"]
    STATUS_ORDER = ["已记录", "待复核", "异常", "已归档"]
    ACTION_RULES = {"提交复核": "待复核", "标记异常": "异常", "归档轨迹": "已归档"}
    NEGATIVE_ACTIONS = []
