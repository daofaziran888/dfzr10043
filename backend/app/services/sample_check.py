"""__NAME__领域服务：字段、状态和动作来自业务配置，数据处理骨架由基类复用。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class SampleCheckService(BaseModuleService):
    MODULE = "sample_check"
    ENTITY = "抽检样本"
    OPERATION_TERM = "关联"
    LIST_FIELDS = ["样本编号", "关联批次", "抽样比例", "抽样行数", "字段通过率", "缺陷描述", "抽检结论", "抽检时间"]
    REQUIRED_FIELDS = ["样本编号", "关联批次", "抽样比例"]
    STATUS_ORDER = ["待抽检", "抽检中", "已通过", "已驳回"]
    ACTION_RULES = {"启动抽检": "抽检中", "通过样本": "已通过", "驳回样本": "已驳回"}
    NEGATIVE_ACTIONS = ["驳回样本"]
