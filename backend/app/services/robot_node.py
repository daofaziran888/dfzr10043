"""机器人节点服务：注册管理、健康心跳、负载与降级。

维护执行端节点的注册信息、并发额度和心跳负载，
决定任务队列能否派发到该节点。超时无心跳的节点自动离线。
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from app.services.base import BaseModuleService


class RobotNodeService(BaseModuleService):
    MODULE = "robot_node"
    ENTITY = "执行节点"
    OPERATION_TERM = "调度"
    LIST_FIELDS = [
        "节点编号", "节点名称", "运行环境", "并发额度", "心跳间隔",
        "当前负载", "领取任务数", "最近心跳",
    ]
    REQUIRED_FIELDS = ["节点编号", "节点名称", "运行环境"]
    STATUS_ORDER = ["待注册", "在线", "降级", "离线"]
    ACTION_RULES = {"注册上线": "在线", "降级限流": "降级", "摘除节点": "离线"}
    NEGATIVE_ACTIONS = ["摘除节点"]

    def heartbeat(self, node_id: int) -> dict[str, Any]:
        """更新节点心跳。"""
        entry = self.get_entry(node_id)
        if entry is None:
            return {"ok": False, "reason": "节点不存在"}
        now = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")
        entry["最近心跳"] = now
        return {"ok": True, "node_id": node_id, "heartbeat": now}

    def check_online_nodes(self, heartbeat_timeout_s: int = 60) -> list[dict[str, Any]]:
        """获取心跳正常在线的节点列表。"""
        items, _ = self.list_entries(size=10000)
        now = datetime.now(timezone(timedelta(hours=8)))
        online = []
        for it in items:
            if it.get("status") != "在线":
                continue
            last = it.get("最近心跳", "")
            try:
                last_dt = datetime.fromisoformat(last)
                if last_dt.tzinfo is None:
                    last_dt = last_dt.replace(tzinfo=timezone(timedelta(hours=8)))
                if (now - last_dt).total_seconds() > heartbeat_timeout_s:
                    self.run_action(it["id"], "摘除节点")
                    continue
            except (ValueError, TypeError):
                pass
            online.append(it)
        return online

    def get_load_balance_candidate(self) -> dict[str, Any] | None:
        """获取负载最低的在线节点供任务派发。"""
        online = self.check_online_nodes()
        if not online:
            return None
        online.sort(key=lambda n: int(n.get("当前负载", "0") or "0"))
        return online[0]