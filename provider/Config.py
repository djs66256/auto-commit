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
        
class GlobalConfig:
    DEFUALT_FILE = f"{os.path.dirname(__file__)}/../config.yml"
    USER_FILE = f'{os.getenv("HOME")}/.auto-commit/config.yml'
    
    def __init__(self):
        with open(self.DEFUALT_FILE) as f:
            self.default_config = yaml.load(f, Loader=yaml.FullLoader)
        if os.path.exists(self.USER_FILE):
            with open(self.USER_FILE) as f:
                self.user_config = yaml.load(f, Loader=yaml.FullLoader)
        else:
            self.user_config = {}

    def getExConfig(self, ex_config):
        path = f"{os.path.dirname(__file__)}/../config.{ex_config}.yml"
        if os.path.exists(path):
            with open(path) as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        return None
    
    def getConfig(self, provider, ex_config = None):
        base_user_config = self.user_config.get("base") or {}
        base_default_config = self.default_config.get("base") or {}
        base_ex_config = {}
        if ex_config:
            base_ex_config = self.getExConfig(ex_config) or {}
        user_config = self.user_config.get(provider) or {}
        default_config = self.default_config.get(provider) or {}
        merged_config = {**base_default_config, **base_user_config, **base_ex_config, **default_config, **user_config}
        return ProviderConfig(provider, merged_config)

if __name__ == "__main__":
    config = GlobalConfig()
    print(config.default_config)
    print(config.getConfig("chatglm").config)