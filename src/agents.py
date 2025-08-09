from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_community.llms import Tongyi
from langchain_community.embeddings import DashScopeEmbeddings
from .prompts import *
from dotenv import load_dotenv
import os
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from .structure_outputs import CategorizeReviewOutput, VerifyReplyOutput, ReplyOutput
from langgraph.prebuilt import create_react_agent
load_dotenv()


class Agents():
    def __init__(self):
        # 大模型
        qwen = Tongyi(model_name="qwen-turbo",datemperature=0.1)
        #写回复agent
        self.reply_agent = create_react_agent(
            model=Tongyi(model_name="qwen-turbo",datemperature=0.1),
            tools=[],
            prompt=SystemMessage(REPLY_REVIEW_PROMPT)

        )
        #评论分类agent
        self.review_category_agent = create_react_agent(
            model=Tongyi(model_name="qwen-turbo", datemperature=0.1),
            tools=[],
            prompt=SystemMessage(CATEGORIZE_REVIEW_PROMPT)
        )
        #审核评论agent
        self.reply_verify_agent = create_react_agent(
            model=Tongyi(model_name="qwen-turbo", datemperature=0.1),
            tools=[],
            prompt=SystemMessage(VERIFY_REPLY_PROMPT)
        )
        # 嵌入模型
        embeddings = DashScopeEmbeddings(
            model="text-embedding-v4", dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
        )
        #结果解析器
        categorizeReviewOutputparser = JsonOutputParser(pydantic_object=CategorizeReviewOutput)
        verifyReplyOutputparser = JsonOutputParser(pydantic_object=VerifyReplyOutput)
        replyOutputparser = JsonOutputParser(pydantic_object=ReplyOutput)

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
        reply_prompt = PromptTemplate(
            template=REPLY_REVIEW_PROMPT,
            input_variables=["current_review","review_category"],
            partial_variables={"format_instructions": verifyReplyOutputparser.get_format_instructions()}

        )


        # 评论分类（差评，好评,产品咨询）
        self.categorize_review = (
                review_category_prompt | qwen | categorizeReviewOutputparser
        )

        self.verify_reply = (
                verify_reply_prompt | qwen  | verifyReplyOutputparser
        )
        self.write_reply = (
            reply_prompt | qwen | replyOutputparser
        )