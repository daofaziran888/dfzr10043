"""凭据保管服务：密文存储、轮换周期管理、失效告警和审计。

凭据信息不散落在流程定义中，由本模块集中保管账号标识、
凭据类型、轮换周期等，并记录使用次数供失效预测。
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from app.services.base import BaseModuleService


class CredentialVaultService(BaseModuleService):
    MODULE = "credential_vault"
    ENTITY = "登录凭据"
    OPERATION_TERM = "存储"
    LIST_FIELDS = [
        "凭据编号", "适用站点", "账号标识", "凭据类型", "轮换周期",
        "最近轮换", "失效标记", "使用次数",
    ]
    REQUIRED_FIELDS = ["凭据编号", "适用站点", "账号标识"]
    STATUS_ORDER = ["待录入", "可用", "临近失效", "已吊销"]
    ACTION_RULES = {"录入凭据": "可用", "触发轮换": "临近失效", "吊销凭据": "已吊销"}
    NEGATIVE_ACTIONS = []

    def check_expiry(self, cred_id: int) -> dict[str, Any]:
        """检查凭据是否临近失效：根据上次轮换时间和轮换周期判断。"""
        entry = self.get_entry(cred_id)
        if entry is None:
            return {"expiring": False, "reason": "凭据不存在"}
        last_rotation = entry.get("最近轮换", "")
        cycle_str = entry.get("轮换周期", "90")
        try:
            cycle_days = int(cycle_str)
        except (ValueError, TypeError):
            cycle_days = 90
        now = datetime.now(timezone(timedelta(hours=8)))
        try:
            last_dt = datetime.fromisoformat(last_rotation)
        except (ValueError, TypeError):
            last_dt = now - timedelta(days=cycle_days + 1)
        days_elapsed = (now - last_dt).days
        if days_elapsed >= cycle_days * 0.8:
            return {
                "expiring": True,
                "cred_id": cred_id,
                "days_elapsed": days_elapsed,
                "cycle_days": cycle_days,
                "action": "建议触发轮换",
            }
        return {"expiring": False, "cred_id": cred_id, "days_elapsed": days_elapsed}

    def get_available_credentials(self, site: str | None = None) -> list[dict[str, Any]]:
        """获取可用的凭据列表，可按站点筛选。"""
        items, _ = self.list_entries(size=10000)
        available = [it for it in items if it.get("status") == "可用"]
        if site:
            available = [it for it in available if it.get("适用站点") == site]
        return available

    def record_usage(self, cred_id: int) -> dict[str, Any]:
        """记录凭据使用次数递增。"""
        entry = self.get_entry(cred_id)
        if entry is None:
            return {"ok": False, "reason": "凭据不存在"}
        count = int(entry.get("使用次数", "0") or "0")
        entry["使用次数"] = str(count + 1)
        return {"ok": True, "cred_id": cred_id, "usage_count": count + 1}