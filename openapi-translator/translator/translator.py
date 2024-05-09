from typing import Optional
from utils.logger import LOG
from .parser import create_parser
from book import Content, ContentType

from translator.writer import Writer


class Translator:
    def __init__(self, model):
        self.model = model
        self.book = None
        LOG.info(f"translator init")

    def translate_text(self, text: str, target_language: str) -> str:
        LOG.info(f"translate text='{text},target_language='{target_language}'")
        prompt = self.model.translate_prompt(Content(ContentType.TEXT, original=text), target_language)
        LOG.info(f"translate prompt='{prompt}'")
        translation, status = self.model.make_request(prompt)
        LOG.info(f"translate result='{translation},{status}'")
        return translation

    def translate(self, file_path: str, target_language: str, file_format: str = None, output_file_path: str = None,
                  pages: Optional[int] = None):
        LOG.info(f"translate file='{file_path}, model='{self.model}'")
        # 根据文件类型创建解析器
        parser = create_parser(file_path)
        self.book = parser.parse(file_path, pages)
        self.writer = Writer()

        for page_idx, page in enumerate(self.book.pages):
            for content_idx, content in enumerate(page.content):
                prompt = self.model.translate_prompt(content, target_language)
                LOG.info(f"translate prompt='{prompt}'")
                translation, status = self.model.make_request(prompt)
                LOG.info(f"translate result='{translation},{status}'")

                self.book.pages[page_idx].content[content_idx].set_translation(translation, status)

        self.writer.save_translated_book(self.book, output_file_path, file_format)
