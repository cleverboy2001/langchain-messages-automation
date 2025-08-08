from pydantic import BaseModel, Field
from typing import List
from enum import Enum

# **Categorize  Output**
class ReviewCategory(str, Enum):
    negative_review = "negative_review"
    positive_review = "positive_review"
    consultation_review = "consultation_review"


#限制大模型输出中必须包含的字段category
class CategorizeReviewOutput(BaseModel):
    category: ReviewCategory = Field(
        ...,
        description="评论所属分类，基于预设规则标识其类型"
    )

# **Reply Writer**
class ReplyOutput(BaseModel):
    reply: str = Field(
        ...,
        description="根据评论分类，做出不同的回复"
    )

class VerifyReplyOutput(BaseModel):
    reason: str = Field(description="审核不通过原因")
    is_rewrite: bool = Field(description="是否需要重写")

# **RAG Query Output**
class RAGQueriesOutput(BaseModel):
    queries: List[str] = Field(
        ...,
        description="根据用户咨询的内容，查询向量库存，获取topK信息"
    )

