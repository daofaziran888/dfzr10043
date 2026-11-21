"""__NAME__领域服务：字段、状态和动作来自业务配置，数据处理骨架由基类复用。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class VersionReleaseService(BaseModuleService):
    MODULE = "version_release"
    ENTITY = "发布版本"
    OPERATION_TERM = "关联"
    LIST_FIELDS = ["发布编号", "关联模板", "版本号", "变更摘要", "灰度比例", "回滚版本", "发布人标识", "发布时间"]
    REQUIRED_FIELDS = ["发布编号", "关联模板", "版本号"]
    STATUS_ORDER = ["待发布", "灰度中", "全量发布", "已回滚"]
    ACTION_RULES = {"启动灰度": "灰度中", "全量发布": "全量发布", "执行回滚": "已回滚"}
    NEGATIVE_ACTIONS = []
