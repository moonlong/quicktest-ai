import os

from book import Book, ContentType
from utils.logger import LOG


class Writer:
    def __init__(self):
        pass

    def save_translated_book(self, book: Book, output_file_path: str = None, file_format: str = None):
        if file_format is None:
            file_format = "markdown"
        if file_format.lower() == "markdown":
            self._save_markdown_book(book, output_file_path)
        elif file_format.lower() == "pdf":
            pass
        else:
            raise ValueError(f"Invalid file format,{file_format}")

    def _save_markdown_book(self, book: Book, output_file_path: str = None):
        if output_file_path is None:
            output_file_path = book.file_path.replace('.pdf', f'_translated.md')

        LOG.info(f"out_file_path: {output_file_path}")
        with open(output_file_path, "w", encoding="utf-8") as f:
            for page in book.pages:
                for content in page.content:
                    if content.status:
                        if content.content_type == ContentType.TEXT:
                            f.write(content.translation + '\n\n')
                        elif content.content_type == ContentType.TABLE:
                            # Add table to the Markdown file
                            table = content.translation
                            header = '|' + '| '.join(str(column) for column in table.columns) + ' |' + '\n'
                            separator = '|' + '| '.join(['---'] * len(table.columns)) + ' |' + '\n'
                            body = '\n'.join(['|' + '| '.join(str(cell) for cell in row) + '|' for row in table.values.tolist()]) + '\n\n'
                            f.write(header + separator + body)
                            # f.write(header + body)


    def _save_pdf_book(self, book: Book, output_file_path: str = None):
        pass
