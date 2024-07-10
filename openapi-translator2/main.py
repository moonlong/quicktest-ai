# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import os
import sys
from utils import ArgumentParser, LOG
from translator import TranslationConfig
from translator import PDFTranslator

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 解析命令行k
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()
    LOG.debug(args)

    config = TranslationConfig()
    config.initialize(args)

    translator = PDFTranslator(config.model_name)
    translator = translator.translate_pdf(config.input_file,
                                          config.output_file_format,
                                          config.source_language,
                                          config.target_language,
                                          pages=None)




