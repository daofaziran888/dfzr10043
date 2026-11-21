"""抽检样本服务：抽样检查、字段通过率和缺陷记录。

对已确认批次做抽样检查，记录字段通过率和缺陷描述，
驳回后批次不得进入交接。支持按比例和行数两种抽样方式。
"""
from __future__ import annotations

from typing import Any

from app.services.base import BaseModuleService


class SampleCheckService(BaseModuleService):
    MODULE = "sample_check"
    ENTITY = "抽检样本"
    OPERATION_TERM = "关联"
    LIST_FIELDS = [
        "样本编号", "关联批次", "抽样比例", "抽样行数", "字段通过率",
        "缺陷描述", "抽检结论", "抽检时间",
    ]
    REQUIRED_FIELDS = ["样本编号", "关联批次", "抽样比例"]
    STATUS_ORDER = ["待抽检", "抽检中", "已通过", "已驳回"]
    ACTION_RULES = {"启动抽检": "抽检中", "通过样本": "已通过", "驳回样本": "已驳回"}
    NEGATIVE_ACTIONS = ["驳回样本"]

    def accept_sample(self, sample_id: int) -> dict[str, Any]:
        """通过抽检样本。"""
        entry = self.get_entry(sample_id)
        if entry is None:
            return {"ok": False, "reason": "样本不存在"}
        self.run_action(sample_id, "通过样本")
        return {"ok": True, "sample_id": sample_id}

    def reject_sample(self, sample_id: int, defect: str) -> dict[str, Any]:
        """驳回抽检样本，记录缺陷描述。"""
        entry = self.get_entry(sample_id)
        if entry is None:
            return {"ok": False, "reason": "样本不存在"}
        entry["缺陷描述"] = defect
        entry["抽检结论"] = "驳回"
        self.run_action(sample_id, "驳回样本")
        return {"ok": True, "sample_id": sample_id, "defect": defect}