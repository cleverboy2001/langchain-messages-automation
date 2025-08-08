from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_community.llms import Tongyi
from langchain_community.embeddings import DashScopeEmbeddings
from .prompts import *
from dotenv import load_dotenv
import os
from langchain_core.output_parsers import JsonOutputParser
from .structure_outputs import CategorizeReviewOutput, VerifyReplyOutput

load_dotenv()


class Agents():
    def __init__(self):
        # 大模型
        qwen = Tongyi(model_name="qwen-turbo",datemperature=0.1)
        kimi = Tongyi(model_name="Moonshot-Kimi-K2-Instruct", temperature=0.1)

        categorizeReviewOutputparser = JsonOutputParser(pydantic_object=CategorizeReviewOutput)
        verifyReplyOutputparser = JsonOutputParser(pydantic_object=VerifyReplyOutput)
        # 嵌入模型
        embeddings = DashScopeEmbeddings(
            model="text-embedding-v4", dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
        )

        # 评论分类的提示词模板
        review_category_prompt = PromptTemplate(
            template=CATEGORIZE_REVIEW_PROMPT,
            input_variables=["review"],
            partial_variables={"format_instructions": categorizeReviewOutputparser.get_format_instructions()}

        )

        verify_reply_prompt = PromptTemplate(
            template=VERIFY_REPLY_PROMPT,
            input_variables=["generated_reply"],
            partial_variables={"format_instructions": verifyReplyOutputparser.get_format_instructions()}

        )


        # 评论分类（差评，好评,产品咨询）
        self.categorize_review = (
                review_category_prompt | qwen | categorizeReviewOutputparser
        )

        self.verify_reply = (
                verify_reply_prompt | qwen  | verifyReplyOutputparser
        )