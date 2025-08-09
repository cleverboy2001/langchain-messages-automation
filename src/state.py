from typing import List
from typing_extensions import TypedDict

class GraphState(TypedDict):
    reviews: List[str]
    current_review: str
    review_category: str
    generated_reply: str
    #是否需要重写
    is_rewrite: bool
    review_reply: List[dict]
    #迭代次数
    trials: int
    is_end: bool