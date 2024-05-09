import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse


from translator.translator import Translator
from model.openai_model import OpenAIModel

# 假设的翻译服务URL
TRANSLATION_SERVICE_URL = "http://0.0.0.0:8000/translate"

app = FastAPI()


# 定义请求模型
class TextTranslationRequest(BaseModel):
    text: str
    lang: str


# 创建一个POST接口，接收一段文本并返回翻译后的文本
@app.post("/translate/")
async def translate_text(request: TextTranslationRequest) -> str:
    try:
        translator = Translator(OpenAIModel("gpt-3.5-turbo", ""))
        result = translator.translate_text(request.text, request.lang)
        return JSONResponse(content={"translatedText": result})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
