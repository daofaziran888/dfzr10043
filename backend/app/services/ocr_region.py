"""__NAME__领域服务：字段、状态和动作来自业务配置，数据处理骨架由基类复用。"""
from __future__ import annotations

from app.services.base import BaseModuleService


class OcrRegionService(BaseModuleService):
    MODULE = "ocr_region"
    ENTITY = "识别区域"
    OPERATION_TERM = "关联"
    LIST_FIELDS = ["区域编号", "关联模板", "区域名称", "坐标范围", "识别引擎", "语言设定", "平均置信度", "最近识别"]
    REQUIRED_FIELDS = ["区域编号", "关联模板", "区域名称"]
    STATUS_ORDER = ["待标定", "已标定", "置信偏低", "已停用"]
    ACTION_RULES = {"标定区域": "已标定", "标记低置信": "置信偏低", "停用区域": "已停用"}
    NEGATIVE_ACTIONS = ["停用区域"]
