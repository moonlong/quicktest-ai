import yaml


class TranslationConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TranslationConfig, cls).__new__(cls)
            cls._instance._config = None
        return cls._instance

    def initialize(self, args):
        with open(args.config_file, 'r') as f:
            config = yaml.safe_load(f)

        override_values = {
            key: value for key, value in vars(args).items() if key in config and value is not None
        }
        config.update(override_values)

        self._instance._config = config

    def __getattr__(self, name):
        if self._instance._config and name in self._instance._config:
            return self._instance._config[name]
        raise AttributeError(f"'TranslationConfig' object has no attribute '{name}'")
