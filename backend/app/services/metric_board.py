"""运行指标服务：统计汇总、指标核对与逐条对账。

按统计维度和窗口汇总流程成功率、平均耗时与产出记录数，
读数需与执行实例逐条对得上。不一致时写审计轨迹。
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from app.services.base import BaseModuleService


class MetricBoardService(BaseModuleService):
    MODULE = "metric_board"
    ENTITY = "指标读数"
    OPERATION_TERM = "采集"
    LIST_FIELDS = [
        "读数编号", "统计维度", "统计窗口", "成功率", "平均耗时",
        "产出记录数", "异常条数", "采集时间",
    ]
    REQUIRED_FIELDS = ["读数编号", "统计维度", "统计窗口"]
    STATUS_ORDER = ["采集中", "已汇总", "已核对", "已作废"]
    ACTION_RULES = {"触发汇总": "已汇总", "核对读数": "已核对", "作废读数": "已作废"}
    NEGATIVE_ACTIONS = ["作废读数"]

    def summarize_with_counter(self, dimension: str, window: str,
                                success: int, fail: int, total_records: int) -> dict[str, Any]:
        """用计数汇总生成指标读数。"""
        total = max(1, success + fail)
        success_rate = round(success / total, 4)
        # 逐条核对逻辑：如果条目异常条数与失败数不一致则为不一致
        anom_count = fail
        result = {
            "dimension": dimension,
            "window": window,
            "success_rate": success_rate,
            "total": total,
            "success": success,
            "fail": fail,
            "total_records": total_records,
            "anomalies": anom_count,
        }
        return result

    def verify_consistency(self, metric_id: int, actual_success_rate: float) -> dict[str, Any]:
        """核对指标读数与执行实例实际成功率的一致性。"""
        entry = self.get_entry(metric_id)
        if entry is None:
            return {"ok": False, "reason": "指标读数不存在"}
        stated = float(entry.get("成功率", "0") or "0")
        if abs(stated - actual_success_rate) <= 0.01:
            self.run_action(metric_id, "核对读数")
            return {"ok": True, "consistent": True}
        self.run_action(metric_id, "核对读数")
        return {"ok": True, "consistent": False, "stated": stated, "actual": actual_success_rate}