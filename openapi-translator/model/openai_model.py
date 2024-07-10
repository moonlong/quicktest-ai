import requests
import simplejson
import os
import time
import openai

from model import Model
from utils.logger import LOG
from openai import OpenAI


class OpenAIModel(Model):
    def __init__(self, model: str, api_key: str = ""):
        self.model = model
        self.api_key = api_key
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        super().__init__()

    def make_request(self, prompt):
        attempts = 0
        while attempts < 3:
            try:
                if self.model == "gpt-3.5-turbo":
                    LOG.info("Using gpt-3.5-turbo model")
                    resp = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "user", "content": prompt}
                        ])
                    return resp.choices[0].message.content.strip(), True
                else:
                    LOG.error(f"Invalid model name,{self.model}")
                    return "", False
            except openai.RateLimitError as e:
                attempts += 1
                if attempts < 3:
                    LOG.warning(f"Rate limit exceeded. Retrying in 1 second. Attempt {attempts}/3")
                    time.sleep(60)
                else:
                    LOG.error(f"Rate limit exceeded. Maximum retries reached. Error: {e}")
            except openai.APIConnectionError as e:
                LOG.error(f"The server could not be reached. Error: {e}")
            except openai.APIStatusError as e:
                LOG.error(f"The server returned an unexpected status code. Error: {e}")
            except Exception as e:
                LOG.error(f"An unexpected error occurred. Error: {e}")

        return "", False
