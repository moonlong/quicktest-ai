from typing import Optional
from translator.pdf_parser import PDFParser
from translator.writer import Writer
from translator.translation_chain import TranslationChain
from utils import LOG

class PDFTranslator:
    def __init__(self, model_name: str):
        self.translation_chain = TranslationChain(model_name=model_name)
        self.pdf_parser = PDFParser()
        self.writer = Writer()

    def translate_pdf(self,
                      input_file: str,
                      output_file_format: str = 'markdown',
                      source_language: str = 'English',
                      target_language: str = 'Chinese',
                      pages: Optional[int] = None) -> object:

        self.book = self.pdf_parser.parse_pdf(input_file, pages)

        for page_index, page in enumerate(self.book.pages):
            for content_index, content in enumerate(page.contents):
                # Translate content.original
                translation, status = self.translation_chain.run(content, source_language, target_language)

                # Update the content in self.book.pages directly
                self.book.pages[page_index].contents[content_index].set_translation(translation, status)

        return self.writer.save_translated_book(self.book, output_file_format)
