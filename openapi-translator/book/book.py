from .page import Page


class Book:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.pages = []

    def add_page(self, page: Page):
        self.pages.append(page)
