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
        workflow.add_node("select_current_review", nodes.select_current_review)
        workflow.add_node("categorize_review", nodes.categorize_review)
        workflow.add_node("route_reply_based_on_category",nodes.route_reply_based_on_category)
        workflow.add_node("reply_positive_review", nodes.reply_positive_review)
        workflow.add_node("reply_negative_review", nodes.reply_negative_review)
        workflow.add_node("reply_consultation_review", nodes.reply_consultation_review)
        workflow.add_node("verify_reply", nodes.verify_reply)
        workflow.add_node("check_status", nodes.is_end)
        workflow.add_node("end", nodes.end)

        workflow.set_entry_point("collect_reviews")

        workflow.add_edge("collect_reviews", "select_current_review")
        workflow.add_edge("select_current_review", "categorize_review")
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

        def route_after_verify(state: GraphState) -> str:
            if not state.get("is_rewrite", False):
                return "check_status"  # 无需重写，检查是否结束
            else:
                # 需要重写时，根据分类返回对应节点
                category = state.get("review_category")
                return {
                    "positive_review": "reply_positive_review",
                    "negative_review": "reply_negative_review",
                    "consultation_review": "reply_consultation_review"
                }.get(category, "check_status")  # 默认 fallback

        workflow.add_conditional_edges(
            source="verify_reply",
            path=route_after_verify  # ✅ 使用独立函数
        )

        workflow.add_conditional_edges(
            source="check_status",
            # 条件判断函数：返回state["is_end"]的值
            path=lambda state: state["is_end"],
            # 条件为True时的目标节点
            path_map={
                True:"end",
                False:"select_current_review"

            }
        )


        # Compile
        self.app = workflow.compile()