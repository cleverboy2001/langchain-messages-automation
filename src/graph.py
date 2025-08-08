from langgraph.graph import END, StateGraph
from .state import GraphState
from .nodes import Nodes

class Workflow():
    def __init__(self):
        # initiate graph state & nodes
        workflow = StateGraph(GraphState)
        nodes = Nodes()

        # define all graph nodes
        workflow.add_node("collect_reviews", nodes.collect_reviews)
        workflow.add_node("categorize_review", nodes.categorize_review)
        workflow.add_node("reply_positive_review", nodes.reply_positive_review)
        workflow.add_node("reply_negative_review", nodes.reply_negative_review)
        workflow.add_node("reply_consultation_review", nodes.reply_consultation_review)
        workflow.add_node("verify_reply", nodes.verify_reply)
        workflow.add_node("end", nodes.end)

        workflow.set_entry_point("collect_reviews")

        workflow.add_edge("collect_reviews", "categorize_review")
        workflow.add_conditional_edges(
            "categorize_review",
            nodes.route_reply_based_on_category,
            {
                "positive_reply": "reply_positive_review",
                "negative_reply": "reply_negative_review",
                "consultation_reply": "reply_consultation_review",
            }
        )


        workflow.add_edge("reply_positive_review", "verify_reply")

        workflow.add_edge("reply_negative_review", "verify_reply")

        workflow.add_edge("reply_consultation_review", "verify_reply")

       #TODO:拆分出一个路由函数
        workflow.add_conditional_edges(
            "verify_reply",
            lambda state: {
                False: "end",  # is_rewrite=False 时结束
                True: {  # is_rewrite=True 时根据 review_category 路由
                    "positive_review": "reply_positive_review",
                    "negative_review": "reply_negative_review",
                    "consultation_review": "reply_consultation_review"
                }.get(state["review_category"], "end")  # 默认返回end
            }[state["is_rewrite"]]
        )


        # Compile
        self.app = workflow.compile()