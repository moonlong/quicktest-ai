from langchain_openai import ChatOpenAI
# from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain.globals import set_verbose, set_debug

from utils import LOG
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate


class TranslationChain:
    def __init__(self, model_name="gpt-3.5-turbo", verbose=True):
        # debug
        set_debug(verbose)
        set_verbose(verbose)

        # 翻译任务指令始终由 System 角色承担
        template = (
            """You are a translation expert, proficient in various languages. \n
            Translates {source_language} to {target_language}."""
        )
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)

        # 待翻译文本由 HumGan 角色输入
        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        # 使用 System 和 Human 角色的提示模板构造 ChatPromptTemplate
        chat_prompt_template = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        # 为了翻译结果的稳定性，将 temperature 设置为 0
        chat = ChatOpenAI(model=model_name, temperature=0, verbose=verbose)

        # self.chain = LLMChain(llm=chat, prompt=chat_prompt_template, verbose=verbose)
        self.chain = chat_prompt_template | chat | StrOutputParser()

    def run(self, text: str, source_language: str, target_language: str) -> (str, bool):
        result = ""
        try:
            # result = self.chain.run({
            result = self.chain.invoke({
                "text": text, "source_language": source_language,
                "target_language": target_language,
            })
        except Exception as e:
            LOG.error(f"An error occurred during translation: {e}")
            return result, False

        return result, True


if __name__ == "__main__":
    tmp = TranslationChain()
    print(tmp.run("I love python", "en", "zh-CN"))
