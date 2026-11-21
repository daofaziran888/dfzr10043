"""__NAME__领域服务：字段、状态和动作来自业务配置，数据处理骨架由基类复用。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class ResourcePoolService(BaseModuleService):
    MODULE = "resource_pool"
    ENTITY = "资源额度"
    OPERATION_TERM = "校验"
    LIST_FIELDS = ["额度编号", "资源类型", "总额度", "已占用", "预留额度", "释放策略", "抢占优先级", "最近调整"]
    REQUIRED_FIELDS = ["额度编号", "资源类型", "总额度"]
    STATUS_ORDER = ["充足", "紧张", "耗尽", "已冻结"]
    ACTION_RULES = {"调整额度": "紧张", "冻结资源": "已冻结", "释放预留": "充足"}
    NEGATIVE_ACTIONS = []
