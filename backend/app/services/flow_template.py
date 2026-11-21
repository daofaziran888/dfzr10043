"""__NAME__领域服务：字段、状态和动作来自业务配置，数据处理骨架由基类复用。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class FlowTemplateService(BaseModuleService):
    MODULE = "flow_template"
    ENTITY = "流程模板"
    OPERATION_TERM = "采集"
    LIST_FIELDS = ["模板编号", "流程名称", "起始地址", "步骤数量", "参数列表", "适用站点", "模板版本", "最近调试"]
    REQUIRED_FIELDS = ["模板编号", "流程名称", "起始地址"]
    STATUS_ORDER = ["草稿", "调试中", "已发布", "已下线"]
    ACTION_RULES = {"提交调试": "调试中", "发布模板": "已发布", "下线模板": "已下线"}
    NEGATIVE_ACTIONS = ["下线模板"]
