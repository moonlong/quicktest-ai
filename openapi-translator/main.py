import sys
import os

from model.openai_model import OpenAIModel
from translator.translator import Translator

from utils.logger import LOG
from utils.argument_parser import ArgumentParser

from web.route import app

if __name__ == '__main__':
    LOG.info("Init args.")
    argument_parser = ArgumentParser()
    args = argument_parser.parse_args()
    # LOG.debug(args)

    if args.server == 1:
        # 运行Uvicorn服务器
        import uvicorn

        uvicorn.run(app, host="0.0.0.0", port=8000)
    elif not os.path.exists(args.book):
        model = OpenAIModel(args.openapi_model, args.open_api_key)
        translator = Translator(model)
        LOG.info(f'Start translate to lang={args.lang},model={args.openapi_model},format={args.file_format}')
        translator.translate(args.book, args.lang, pages=1)
