from .APIProvider import APIProvider
from .Config import ProviderConfig
from openai import OpenAI

class OpenAIProvider(APIProvider):

    def __init__(self, config: ProviderConfig):
        super().__init__(config)
        self.base_url = config.get("base_url")
        if self.base_url is None:
            raise Exception("No base url found")
        
        self.api_key = config.get("api_key")
        if self.api_key is None:
            raise Exception("No api key found")
        if self.api_key == "":
            raise Exception("No api key found")
        
        self.model = config.get("model")
        if self.model is None:
            raise Exception("No model found")

    def generate_message(self, **kargs) -> str:
        prompt = self.render_generate_prompt(**kargs)
        return self.request(prompt)
    
    def summarize(self, **kargs):
        prompt = self.render_generate_prompt(**kargs)
        return self.request(prompt)
        
    def request(self, prompt):
        if prompt is None:
            raise Exception("Render prompt failed")
        
        client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            top_p=0.7,
            temperature=0.9
        )
        return response.choices[0].message.content.replace("```", "")