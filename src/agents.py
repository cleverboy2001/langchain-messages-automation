from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_community.llms import Tongyi
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.embeddings import DashScopeEmbeddings
from .prompts import *
from dotenv import load_dotenv
import os

from .structure_outputs import CategorizeReviewOutput, VerifyReplyOutput

load_dotenv()


class Agents():
    def __init__(self):
        # 大模型
        qwen = Tongyi(model_name="qwen-plus",datemperature=0.1)
        kimi = Tongyi(model_name="Moonshot-Kimi-K2-Instruct", temperature=0.1)
        # 嵌入模型
        embeddings = DashScopeEmbeddings(
            model="text-embedding-v4", dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
        )

        # 评论分类的提示词模板
        review_category_prompt = PromptTemplate(
            template=CATEGORIZE_REVIEW_PROMPT,
            input_variables=["review"]
        )


        # 评论分类（差评，好评,产品咨询）
        self.categorize_review = (
                review_category_prompt |
                kimi.with_structured_output(CategorizeReviewOutput)
        )

        self.verify_reply = (
                review_category_prompt |
                qwen.with_structured_output(VerifyReplyOutput)
        )