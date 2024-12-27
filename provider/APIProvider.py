from .Config import ProviderConfig

class APIProvider:
    def __init__(self, config: ProviderConfig):
        self.config = config

    def generate_message(self, **kargs) -> str:
        pass

    def summarize(self, **kargs) -> str:
        pass

    def render_generate_prompt(self, **kargs) -> str:
        return self.config.render("generate_prompt", **kargs)
    
    def render_summarize_prompt(self, **kargs) -> str:
        return self.config.render("summarize_prompt", **kargs)
