import sys
import os

from translator.translator import Translator

from utils.logger import LOG
from utils.argument_parser import ArgumentParser

if __name__ == '__main__':
    LOG.info("Init args.")
    argument_parser = ArgumentParser()
    args = argument_parser.parse_args()
    # LOG.debug(args)

    pdf_file_path = args.book
    if not os.path.exists(pdf_file_path):
        LOG.error("File not exists.")
        sys.exit(1)

    translator = Translator(args.model_type)
    LOG.info(f'Start translate to lang={args.lang},format={args.file_format}')

    translator.translate(pdf_file_path, args.lang, args.pages)
