"""__NAME__领域服务：字段、状态和动作来自业务配置，数据处理骨架由基类复用。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class FlowRunService(BaseModuleService):
    MODULE = "flow_run"
    ENTITY = "执行实例"
    OPERATION_TERM = "采集"
    LIST_FIELDS = ["执行编号", "关联模板", "执行节点", "触发方式", "开始时间", "结束时间", "步骤进度", "产出记录数"]
    REQUIRED_FIELDS = ["执行编号", "关联模板", "执行节点"]
    STATUS_ORDER = ["排队中", "执行中", "已完成", "执行失败"]
    ACTION_RULES = {"派发执行": "执行中", "中止执行": "已完成", "标记失败": "执行失败"}
    NEGATIVE_ACTIONS = []
