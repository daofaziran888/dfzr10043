"""__NAME__领域服务：字段、状态和动作来自业务配置，数据处理骨架由基类复用。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class DataLandingService(BaseModuleService):
    MODULE = "data_landing"
    ENTITY = "落库记录"
    OPERATION_TERM = "采集"
    LIST_FIELDS = ["落库编号", "关联批次", "目标存储", "写入模式", "写入行数", "冲突行数", "落库水位", "完成时间"]
    REQUIRED_FIELDS = ["落库编号", "关联批次", "目标存储"]
    STATUS_ORDER = ["待写入", "写入中", "已写入", "写入异常"]
    ACTION_RULES = {"启动写入": "写入中", "确认写入": "已写入", "标记异常": "写入异常"}
    NEGATIVE_ACTIONS = []
