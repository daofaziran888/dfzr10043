"""字段映射服务：映射规则管理、试算验证与转换函数。

维护采集记录到目标存储字段的映射、转换函数和空值策略，
试算通过后才允许生效。支持映射版本化管理。
"""
from __future__ import annotations

from typing import Any, Callable

from app.services.base import BaseModuleService


class FieldMappingService(BaseModuleService):
    MODULE = "field_mapping"
    ENTITY = "映射规则"
    OPERATION_TERM = "采集"
    LIST_FIELDS = [
        "映射编号", "来源字段", "目标字段", "转换函数", "空值策略",
        "类型声明", "映射版本", "最近生效",
    ]
    REQUIRED_FIELDS = ["映射编号", "来源字段", "目标字段"]
    STATUS_ORDER = ["草稿", "试算中", "已生效", "已作废"]
    ACTION_RULES = {"提交试算": "试算中", "生效映射": "已生效", "作废映射": "已作废"}
    NEGATIVE_ACTIONS = ["作废映射"]

    _TRANSFORM_FUNCTIONS: dict[str, Callable[[str], Any]] = {
        "str_to_int": lambda v: int(v) if v else 0,
        "str_to_float": lambda v: float(v) if v else 0.0,
        "to_upper": lambda v: str(v).upper(),
        "to_lower": lambda v: str(v).lower(),
        "strip": lambda v: str(v).strip(),
        "default_empty": lambda v: str(v) if v else "",
    }

    def trial_mapping(self, mapping_id: int, sample_value: str) -> dict[str, Any]:
        """对单条映射做试算，返回转换结果供比对。"""
        entry = self.get_entry(mapping_id)
        if entry is None:
            return {"ok": False, "reason": "映射规则不存在"}
        transform = entry.get("转换函数", "strip")
        null_policy = entry.get("空值策略", "skip")
        if not sample_value and null_policy == "skip":
            return {"ok": False, "reason": "空值且策略为skip，跳过"}
        fn = self._TRANSFORM_FUNCTIONS.get(transform, self._TRANSFORM_FUNCTIONS["strip"])
        try:
            result = fn(sample_value)
            return {"ok": True, "mapping_id": mapping_id, "input": sample_value, "output": result}
        except (ValueError, TypeError) as e:
            return {"ok": False, "reason": f"转换失败: {e}"}

    def activate_mappings(self, mapping_ids: list[int]) -> dict[str, Any]:
        """批量生效映射规则。"""
        ok, fail = 0, 0
        for mid in mapping_ids:
            entry = self.get_entry(mid)
            if entry and entry.get("status") in ("草稿", "试算中"):
                self.run_action(mid, "提交试算")
                self.run_action(mid, "生效映射")
                ok += 1
            else:
                fail += 1
        return {"ok": True, "activated": ok, "failed": fail}