from .agents import Agents
from .state import GraphState
from .tools.collectReviewsTools import ReviewToolsClass
from .tools.dbTools import DbToolsClass
from colorama import Fore, Style


class Nodes:
    def __init__(self):
        self.agents = Agents()
        # self.db_tools = DbToolsClass()
        #self.review_tools = ReviewToolsClass()

    #评论收集
    def collect_reviews(self, state: GraphState) -> GraphState:
         #TODO:后续补充搜集评论的agent
         print(Fore.YELLOW + "搜集评论...\n" + Style.RESET_ALL)
         reviews = ["服务员态度差，脾气暴躁，建议开除","菜品太好吃了，下次还来","你的店铺的招牌菜是啥？下次我来试一试"]
         print(Fore.MAGENTA + f"搜集到的评论:" + Style.RESET_ALL)
         for i, review in enumerate(reviews, 1):
             print(f"{i}. {review}"+ Style.RESET_ALL)

         return {"reviews": reviews}

    #评论分类：1.好评 2.差评 3.咨询评论
    def categorize_review(self, state: GraphState) -> GraphState:
        # 从状态中依次获取评论
        current_review = state["reviews"][0]  # state["emails"] 是邮件列表，[-1] 取最后一个（最新）
        print(Fore.YELLOW + "→ 处理中：" + Style.RESET_ALL + f" {current_review}\n")
        print(Fore.YELLOW + "正在判断当前评论的分类...\n" + Style.RESET_ALL)
        # invoke方法传入评论到提示词中，让大模型分类
        result = self.agents.categorize_review.invoke({"review": current_review})
        # 打印日志：展示分类结果（洋红色文字）
        print(Fore.MAGENTA + f"评论分类: {result["category"]}" + Style.RESET_ALL)
        #返回值添加到state中
        return {
            "review_category": result["category"],
            "current_review": current_review
        }
    #路由节点，根据评论的分类，选择对应生成回复的节点
    def route_reply_based_on_category(self, state: GraphState) -> str:
        print(Fore.YELLOW + "\n正在选择回复{}节点\n".format(state["review_category"]) + Style.RESET_ALL)
        category = state["review_category"]
        if category == "positive_review":
            return "positive_reply"
        elif category == "negative_review":
            return "negative_reply"
        elif category == "consultation_review":
            return "consultation_reply"

    #好评回复
    def reply_positive_review(self, state: GraphState) -> GraphState:
        print(Fore.YELLOW + "宝宝正在高兴地写好评的回复\n" + Style.RESET_ALL)
        #TODO：添加Agent写回复
        trials = state.get('trials', 0) + 1
        print(Fore.MAGENTA + f"AI回复:感谢您对于我们服务或者产品的认可，您的支持是我们前进的动力" + Style.RESET_ALL)
        return {"generated_reply": "感谢您对于我们服务或者产品的认可，您的支持是我们前进的动力", "trials": trials}

    #差评回复
    def reply_negative_review(self, state: GraphState) -> GraphState:
        print(Fore.YELLOW + "牛马正含着泪在回复差评...\n" + Style.RESET_ALL)
        # TODO：添加Agent写回复
        trials = state.get('trials', 0) + 1
        print(Fore.MAGENTA + f"AI回复:对不起，对于您提出问题，我们将派专员在24小时内联系您了解详细情况" + Style.RESET_ALL)
        return {"generated_reply": "对不起，对于您提出问题，我们将派专员在24小时内联系您了解详细情况", "trials": trials}

    #咨询回复结合RAG
    def reply_consultation_review(self, state: GraphState) -> GraphState:
        print(Fore.YELLOW + "俺正在翻书解决小主的疑问\n" + Style.RESET_ALL)
        #TODO:添加Agent写回复结合RAG向量数据库
        trials = state.get('trials', 0) + 1
        return {"generated_reply": "查询RAG中","trials": trials}

     #审核回复
    def verify_reply(self, state: GraphState) -> GraphState:
        print(Fore.YELLOW + "严格审核回复中，一丝不苟~...\n" + Style.RESET_ALL)

        verify_info = self.agents.verify_reply.invoke({
            "generated_reply": state["generated_reply"],
            "review_category": state["review_category"]
        })
        print(f"是否需要重写: {verify_info['is_rewrite']}")
        print(f"原因: {verify_info['reason']}")
        is_rewrite = verify_info["is_rewrite"]
        if state["trials"] >=3:
            return {
                "is_rewrite": False,
                "review_reply": {"review": state["reviews"].pop(0), "reply": "无法生成，请人工回复"}
            }
        if is_rewrite:
            return {"is_rewrite": True}
        else:
            #保存评论和回复
            return {
                "is_rewrite": False,
                "review_reply": {"review": state["reviews"].pop(0), "reply":state["generated_reply"]}
            }

   #结束节点
    def end(self, state: GraphState) -> GraphState:


        return