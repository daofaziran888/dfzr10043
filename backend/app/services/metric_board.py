"""__NAME__领域服务：字段、状态和动作来自业务配置，数据处理骨架由基类复用。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class MetricBoardService(BaseModuleService):
    MODULE = "metric_board"
    ENTITY = "指标读数"
    OPERATION_TERM = "采集"
    LIST_FIELDS = ["读数编号", "统计维度", "统计窗口", "成功率", "平均耗时", "产出记录数", "异常条数", "采集时间"]
    REQUIRED_FIELDS = ["读数编号", "统计维度", "统计窗口"]
    STATUS_ORDER = ["采集中", "已汇总", "已核对", "已作废"]
    ACTION_RULES = {"触发汇总": "已汇总", "核对读数": "已核对", "作废读数": "已作废"}
    NEGATIVE_ACTIONS = ["作废读数"]
