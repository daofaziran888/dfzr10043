"""__NAME__领域服务：字段、状态和动作来自业务配置，数据处理骨架由基类复用。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class FileDropService(BaseModuleService):
    MODULE = "file_drop"
    ENTITY = "归集文件"
    OPERATION_TERM = "关联"
    LIST_FIELDS = ["归集编号", "关联执行", "文件名称", "文件类型", "字节大小", "校验值", "归集目录", "归集时间"]
    REQUIRED_FIELDS = ["归集编号", "关联执行", "文件名称"]
    STATUS_ORDER = ["待归集", "已归集", "校验不符", "已清理"]
    ACTION_RULES = {"触发归集": "已归集", "校验文件": "校验不符", "清理归集": "已清理"}
    NEGATIVE_ACTIONS = []
