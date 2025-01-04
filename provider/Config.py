import os
import yaml
from jinja2 import Template

class ProviderConfig:
    def __init__(self, provider, config):
        self.provider = provider
        self.config = config

    def get(self, key):
        return self.config[key]
    
    def render(self, key, **kwargs):
        template = self.get(key)
        if template is not None:
            return Template(template).render(**kwargs)
        

def get_default_file_path(ex_config = None):
    if ex_config:
        return f"{os.path.dirname(__file__)}/../config.{ex_config}.yml"
    else:
        return f"{os.path.dirname(__file__)}/../config.yml"

def get_user_config_file_path(ex_config = None):
    if ex_config:
        return f'{os.getenv("HOME")}/.auto-commit/config.{ex_config}.yml'
    else:
        return f'{os.getenv("HOME")}/.auto-commit/config.yml'
    

class GlobalConfig:
    def getExConfig(self, ex_config):
        path = f"{os.path.dirname(__file__)}/../config.{ex_config}.yml"
        if os.path.exists(path):
            with open(path) as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        return None
    
    def getConfigFileList(self, ex_config = None):
        if ex_config is None:
            return [
                get_default_file_path(),
                get_user_config_file_path(),
            ]
        else:
            return [
                get_default_file_path(),
                get_default_file_path(ex_config),
                get_user_config_file_path(),
                get_user_config_file_path(ex_config)
            ]
    
    def getConfigInFiles(self, files, key):
        result = {}
        for file in files:
            if os.path.exists(file):
                with open(file) as f:
                    config = yaml.load(f, Loader=yaml.FullLoader)
                    value = config.get(key)
                    if value:
                        result = {**result, **value}
        return result

    def _getConfig(self, key, ex_config = None):
        files = self.getConfigFileList(ex_config)
        return self.getConfigInFiles(files, key)
    
    def getConfig(self, provider, ex_config = None):
        base_config = self._getConfig("base", ex_config)
        provider_config = self._getConfig(provider, ex_config)
        merged_config = {**base_config, **provider_config}
        return ProviderConfig(provider, merged_config)

if __name__ == "__main__":
    config = GlobalConfig()
    print(config.default_config)
    print(config.getConfig("chatglm").config)