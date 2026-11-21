"""文件归集服务：中间文件收集、校验值索引与目录管理。

归集流程运行过程中下载或生成的中间文件，按执行实例建立
目录与校验值索引，校验不符的文件标记后供排查。
"""
from __future__ import annotations

from typing import Any

from app.services.base import BaseModuleService


class FileDropService(BaseModuleService):
    MODULE = "file_drop"
    ENTITY = "归集文件"
    OPERATION_TERM = "存储"
    LIST_FIELDS = [
        "归集编号", "关联执行", "文件名称", "文件类型", "字节大小",
        "校验值", "归集目录", "归集时间",
    ]
    REQUIRED_FIELDS = ["归集编号", "关联执行", "文件名称"]
    STATUS_ORDER = ["待归集", "已归集", "校验不符", "已清理"]
    ACTION_RULES = {"触发归集": "已归集", "校验文件": "校验不符", "清理归集": "已清理"}
    NEGATIVE_ACTIONS = []

    def verify_file(self, file_id: int, expected_checksum: str) -> dict[str, Any]:
        """校验文件完整性：比对校验值，不符则标记校验不符。"""
        entry = self.get_entry(file_id)
        if entry is None:
            return {"ok": False, "reason": "文件不存在"}
        actual = entry.get("校验值", "")
        if actual != expected_checksum:
            self.run_action(file_id, "校验文件")
            return {"ok": True, "file_id": file_id, "match": False}
        return {"ok": True, "file_id": file_id, "match": True}

    def get_files_by_run(self, run_code: str) -> list[dict[str, Any]]:
        """按关联执行获取归集文件列表。"""
        items, _ = self.list_entries(size=10000)
        return [it for it in items if it.get("关联执行") == run_code]