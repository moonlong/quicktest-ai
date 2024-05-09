from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

import pdfplumber

from book import Book, Page, Content, ContentType, TableContent
from utils.logger import LOG


# 定义一个抽象基类，所有的解析器都需要继承这个类
class Parser(ABC):
    @abstractmethod
    def parse(self, file_path: str, pages: Optional[int] = None) -> Book:
        pass


# 具体的解析器类
class PDFParser(Parser):
    def __init__(self):
        LOG.debug("PDF Parser init")

    def __str__(self):
        return "PDF Parser"

    def parse(self, file_path: str, pages: Optional[int] = None) -> Book:
        LOG.info(f"Parsing file: {file_path}")

        result = Book(file_path)
        with pdfplumber.open(file_path) as pdf:
            if pages is not None and pages > len(pdf.pages):
                raise ValueError(f"Pages out of range,total_page={len(pdf.pages)},request page={pages}")
            if pages is None:
                pages_to_parse = pdf.pages
            else:
                pages_to_parse = pdf.pages[0:pages]

            for pdf_page in pages_to_parse:
                page = Page()
                raw_txt = pdf_page.extract_text()
                tables = pdf_page.extract_tables()

                for table_data in tables:
                    for row in table_data:
                        for cell in row:
                            raw_txt = raw_txt.replace(cell, "", 1)

                if raw_txt:
                    raw_txt_lines = raw_txt.splitlines()
                    clean_txt_lines = [line.strip() for line in raw_txt_lines if line.strip()]
                    clean_raw_txt = "\n".join(clean_txt_lines)

                    txt_content = Content(ContentType.TEXT, original=clean_raw_txt)
                    page.add_content(txt_content)
                    LOG.debug(f"[raw_txt]: {clean_raw_txt}")

                if tables:
                    table = TableContent(tables)
                    page.add_content(table)
                    LOG.debug(f"[table]:\n{table}")

                result.add_page(page)

        return result


class FileType(Enum):
    PDF = "pdf"
    Txt = "txt"
    Doc = "doc"
    Excel = "excel"


def get_file_extension(file_name):
    # 使用 str.rsplit 分割字符串，最多分割一次，默认从右侧开始
    return file_name.rsplit('.', 1)[-1]


def create_parser(file_name: str) -> Parser:
    file_type = get_file_extension(file_name)
    if file_type == FileType.PDF.value:
        return PDFParser()
    else:
        raise ValueError("Unsupported file type")
