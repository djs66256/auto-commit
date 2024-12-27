
from .APIProvider import APIProvider
from .Config import GlobalConfig
from .OpenAIProvider import OpenAIProvider

PROVIDERS: dict[str, APIProvider] = {
    "openai": OpenAIProvider,
}

glable_config = GlobalConfig()

def get_provider(provider_name: str) -> APIProvider:
    config = glable_config.getConfig(provider_name)
    # print("========")
    # print(config.config)
    # print("========")
    key = config.get("api_type") or provider_name
    class_ = PROVIDERS[key]
    if class_ is None:
        raise Exception(f"Provider {key} not found")
    return class_(config)

def get_settings():
    return glable_config.getConfig("settings")