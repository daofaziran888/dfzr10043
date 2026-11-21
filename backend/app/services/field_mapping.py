"""__NAME__领域服务：字段、状态和动作来自业务配置，数据处理骨架由基类复用。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class FieldMappingService(BaseModuleService):
    MODULE = "field_mapping"
    ENTITY = "映射规则"
    OPERATION_TERM = "采集"
    LIST_FIELDS = ["映射编号", "来源字段", "目标字段", "转换函数", "空值策略", "类型声明", "映射版本", "最近生效"]
    REQUIRED_FIELDS = ["映射编号", "来源字段", "目标字段"]
    STATUS_ORDER = ["草稿", "试算中", "已生效", "已作废"]
    ACTION_RULES = {"提交试算": "试算中", "生效映射": "已生效", "作废映射": "已作废"}
    NEGATIVE_ACTIONS = ["作废映射"]
