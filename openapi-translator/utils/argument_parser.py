import argparse


class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Translate language')
        self.parser.add_argument("--config", type=str, default="config.yaml",
                                 help="configuration file")
        self.parser.add_argument("--timeout", type=int,
                                 help="time out for the api request in seconds")

        self.parser.add_argument("--model_type", type=str,
                                 choices=["GLMModel", "OpenAIModel"], default='OpenAIModel',
                                 help='the type of translation model to use')
        self.parser.add_argument("--openapi_model", type=str,
                                 default="gpt-3.5-turbo",
                                 help="the model name of OpenAI Model")
        self.parser.add_argument("--open_api_key", type=str,
                                 default='test',
                                 help="The API key for OpenAIModel")

        self.parser.add_argument("--book", type=str, required=True, help="target book")
        self.parser.add_argument("--lang", type=str, default="zh", help="target language")
        self.parser.add_argument("--pages", type=int, help="target book pages")
        self.parser.add_argument("--file_format", type=str,
                                 choices=['PDF', 'Markdown'],
                                 default='Markdown',
                                 help="target file format")

    def parse_args(self):
        args = self.parser.parse_args()
        if args.model_type == "OpenAIModel":
            if not args.openapi_model:
                raise ValueError("openapi_model is required for OpenAIModel")
            if not args.open_api_key:
                raise ValueError("open_api_key is required for OpenAIModel")
        return args
