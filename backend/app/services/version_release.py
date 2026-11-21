"""版本发布服务：灰度发布、全量放开与回滚绑定。

维护流程模板的版本发布记录，回滚后执行实例必须重新绑定旧版本。
支持冲突版本仲裁：回滚场景下旧版本胜出。
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from app.services.base import BaseModuleService


class VersionReleaseService(BaseModuleService):
    MODULE = "version_release"
    ENTITY = "发布版本"
    OPERATION_TERM = "关联"
    LIST_FIELDS = [
        "发布编号", "关联模板", "版本号", "变更摘要", "灰度比例",
        "回滚版本", "发布人标识", "发布时间",
    ]
    REQUIRED_FIELDS = ["发布编号", "关联模板", "版本号"]
    STATUS_ORDER = ["待发布", "灰度中", "全量发布", "已回滚"]
    ACTION_RULES = {"启动灰度": "灰度中", "全量发布": "全量发布", "执行回滚": "已回滚"}
    NEGATIVE_ACTIONS = []

    def resolve_conflict(self, current_version_id: int, rollback_target: str) -> dict[str, Any]:
        """冲突版本仲裁：回滚时旧版本胜出，执行实例绑定旧版本。"""
        current = self.get_entry(current_version_id)
        if current is None:
            return {"ok": False, "reason": "版本不存在"}
        self.run_action(current_version_id, "执行回滚")
        return {
            "ok": True,
            "version_id": current_version_id,
            "current_version": current.get("版本号"),
            "rollback_target": rollback_target,
            "arbitration": "旧版本胜出，回滚执行",
        }

    def get_active_versions(self, template_id: int | None = None) -> list[dict[str, Any]]:
        """获取当前有效的版本列表（灰度中或全量发布状态）。"""
        items, _ = self.list_entries(size=10000)
        active = [it for it in items if it.get("status") in ("灰度中", "全量发布")]
        if template_id is not None:
            active = [it for it in active if str(it.get("关联模板", "")).find(str(template_id)) >= 0]
        return active

    def get_rollback_history(self) -> list[dict[str, Any]]:
        """获取所有已回滚的版本记录，供回滚审计。"""
        items, _ = self.list_entries(size=10000)
        return [it for it in items if it.get("status") == "已回滚"]