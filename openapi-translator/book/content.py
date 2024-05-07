from enum import auto, Enum

import pandas as pd
from PIL import Image as PILImage

from utils.logger import LOG


class ContentType(Enum):
    TEXT = auto()
    TABLE = auto()
    IMAGE = auto()


class Content:
    def __init__(self, content_type: ContentType, original, translation=None):
        self.content_type = content_type
        self.original = original
        self.translation = translation
        self.status = False

    def set_translation(self, translation, status):
        if not self.check_translation(translation):
            raise ValueError(f"Invalid translation type. Expected {self.content_type}, but got {type(translation)}")
        self.translation = translation
        self.status = status

    def check_translation(self, translation):
        if self.content_type == ContentType.TEXT:
            return isinstance(translation, str)
        elif self.content_type == ContentType.TABLE:
            return isinstance(translation, list)
        elif self.content_type == ContentType.IMAGE:
            return isinstance(translation, PILImage.Image)
        else:
            raise ValueError(f"Invalid content type: {self.content_type}")
        return False


class TableContent(Content):
    def __init__(self, data, translation=None):
        df = pd.DataFrame(data)
        # LOG.debug(f"{len(data)},{len(df)}")
        # LOG.debug(f"col: {len(data[0])},{len(df.columns)}")
        if len(data) != len(df) or len(data[0]) != len(df.columns):
            raise ValueError("The number of rows and columns in the extracted table data and DataFrame object do not match.")

        super().__init__(ContentType.TEXT, df, translation)

    def set_translation(self, translation, status):
        try:
            if not isinstance(translation, str):
                raise ValueError("Invalid translation type. Expected str, but got {}".format(type(translation)))

            LOG.debug(translation)

            table_data = [row.strip().split() for row in translation.strip().split("\n")]
            LOG.debug(table_data)
            translate_df = pd.DataFrame(table_data[1:], table_data[0])
            LOG.debug(translate_df)

            self.translation = translate_df
            self.status = status
        except Exception as e:
            LOG.error(f"An error occurred during table translation: {e}")
            self.translation = None
            self.status = False

    def __str__(self):
        return self.original.to_string(Headers=False, index=False)

    def iter_items(self, translated=False):
        target_df = self.original if translated else self.original
        for row_idx, row in target_df.iterrows():
            for col_idx, col in enumerate(row):
                yield row_idx, col_idx, col

    def update_item(self, row_idx, col_idx, value, translated=False):
        target_df = self.original if translated else self.original
        target_df.at[row_idx, col_idx] = value

    def get_original_as_str(self):
        return self.original.to_string(Headers=False, index=False)
