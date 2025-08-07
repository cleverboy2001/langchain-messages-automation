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
        workflow.add_node("verify_positive_reply", nodes.verify_positive_reply)
        workflow.add_node("verify_negative_reply", nodes.verify_negative_reply)
        workflow.add_node("verify_consultation_reply", nodes.verify_consultation_reply)
        workflow.add_node("end", nodes.end)

        # load inbox emails
        workflow.set_entry_point("collect_reviews")

        # check if there are emails to process
        workflow.add_edge("collect_reviews", "categorize_review")
        workflow.add_conditional_edges(
            "categorize_review",
            nodes.categorize_review,
            {
                "positive_review": "reply_positive_review",
                "negative_review": "reply_negative_review",
                "consultation_review": "reply_consultation_review",
            }
        )


        workflow.add_edge("reply_positive_review", "verify_positive_reply")

        workflow.add_edge("reply_negative_review", "verify_negative_reply")

        workflow.add_edge("reply_consultation_review", "verify_consultation_reply")

        workflow.add_conditional_edges(
            "email_proofreader",
            nodes.must_rewrite,
            {
                "send": "send_email",
                "rewrite": "email_writer",
                "stop": "categorize_email"
            }
        )

        # check if there are still emails to be processed
        workflow.add_edge("send_email", "is_email_inbox_empty")
        workflow.add_edge("skip_unrelated_email", "is_email_inbox_empty" )

        # Compile
        self.app = workflow.compile()