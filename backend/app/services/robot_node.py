"""__NAME__领域服务：字段、状态和动作来自业务配置，数据处理骨架由基类复用。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class RobotNodeService(BaseModuleService):
    MODULE = "robot_node"
    ENTITY = "执行节点"
    OPERATION_TERM = "校验"
    LIST_FIELDS = ["节点编号", "节点名称", "运行环境", "并发额度", "心跳间隔", "当前负载", "领取任务数", "最近心跳"]
    REQUIRED_FIELDS = ["节点编号", "节点名称", "运行环境"]
    STATUS_ORDER = ["待注册", "在线", "降级", "离线"]
    ACTION_RULES = {"注册上线": "在线", "降级限流": "降级", "摘除节点": "离线"}
    NEGATIVE_ACTIONS = []
