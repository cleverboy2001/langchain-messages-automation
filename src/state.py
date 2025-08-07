from pydantic import BaseModel, Field
from typing import List, Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    reviews: List[str]
    current_review: str
    review_category: str
    generated_reply: str
    #是否需要重写
    is_rewrite: bool
    writer_messages: Annotated[list, add_messages]
    #迭代次数
    trials: int