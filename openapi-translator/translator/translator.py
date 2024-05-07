from typing import Optional
from utils.logger import LOG
from .parser import create_parser


class Translator:
    def __init__(self, model):
        self.model = model
        self.book = None
        LOG.info(f"translator init")

    def translate(self, file_path: str, target_language: str, pages: Optional[int] = None):
        LOG.info(f"translate file='{file_path}, model='{self.model}'")
        # 根据文件类型创建解析器
        parser = create_parser(file_path)
        self.book = parser.parse(file_path, pages)
