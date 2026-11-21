"""__NAME__领域服务：字段、状态和动作来自业务配置，数据处理骨架由基类复用。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class CredentialVaultService(BaseModuleService):
    MODULE = "credential_vault"
    ENTITY = "登录凭据"
    OPERATION_TERM = "存储"
    LIST_FIELDS = ["凭据编号", "适用站点", "账号标识", "凭据类型", "轮换周期", "最近轮换", "失效标记", "使用次数"]
    REQUIRED_FIELDS = ["凭据编号", "适用站点", "账号标识"]
    STATUS_ORDER = ["待录入", "可用", "临近失效", "已吊销"]
    ACTION_RULES = {"录入凭据": "可用", "触发轮换": "临近失效", "吊销凭据": "已吊销"}
    NEGATIVE_ACTIONS = []
