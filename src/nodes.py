from .agents import Agents
from .state import GraphState
from .tools.collectReviewsTools import ReviewToolsClass
from .tools.dbTools import DbToolsClass
from colorama import Fore, Style


class Nodes:
    def __init__(self):
        self.agents = Agents()
        self.db_tools = DbToolsClass()
        self.review_tools = ReviewToolsClass()

    #评论收集
    def collect_reviews(self, state: GraphState) -> GraphState:
         #TODO:后续补充搜集评论的agent


        return {"reviews": ["服务员态度差，脾气暴躁，建议开除","菜品太好吃了，下次还来","你的店铺的招牌菜是啥？下次我来试一试"]}

    #评论分类：1.好评 2.差评 3.咨询评论
    def categorize_review(self, state: GraphState) -> GraphState:
        print(Fore.YELLOW + "Checking email category...\n" + Style.RESET_ALL)
        # 从状态中依次获取评论
        current_review = state["reviews"][0]  # state["emails"] 是邮件列表，[-1] 取最后一个（最新）
        # invoke方法传入评论到提示词中，让大模型分类
        result = self.agents.categorize_review.invoke({"review": current_review})
        # 打印日志：展示分类结果（洋红色文字）
        print(Fore.MAGENTA + f"Review category: {result.category.value}" + Style.RESET_ALL)
        #返回值添加到state中
        return {
            "email_category": result.category.value,
            "current_email": current_review
        }

    #好评回复
    def reply_positive_review(self, state: GraphState) -> GraphState:
        print(Fore.YELLOW + "宝宝正在高兴地写好评的回复\n" + Style.RESET_ALL)
        #TODO：添加Agent写回复
        trials = state.get('trials', 0) + 1
        return {"generated_reply": "感谢您对于我们服务或者产品的认可，您的支持是我们前进的动力", "trials": trials}

    #差评回复
    def reply_negative_review(self, state: GraphState) -> GraphState:
        print(Fore.YELLOW + "牛马正含着泪在写差评的回复...\n" + Style.RESET_ALL)
        # TODO：添加Agent写回复
        trials = state.get('trials', 0) + 1
        return {"generated_reply": "对不起，对于您提出问题，我们会积极解决", "trials": trials}

    #咨询回复结合RAG
    def reply_consultation_review(self, state: GraphState) -> GraphState:
        print(Fore.YELLOW + "俺正在翻书解决小主的疑问\n" + Style.RESET_ALL)
        #TODO:添加Agent写回复结合RAG向量数据库
        trials = state.get('trials', 0) + 1
        return {"generated_reply": "查询RAG中","trials": trials}

     #审核好评回复
    def verify_positive_reply(self, state: GraphState) -> GraphState:
        print(Fore.YELLOW + "严格审核回复中，一丝不苟~...\n" + Style.RESET_ALL)
        is_rewrite = self.agents.verify_reply.invoke({"reply": state.generated_reply})

        return {"is_rewrite": is_rewrite }

    # 审核差评回复
    def verify_negative_reply(self, state: GraphState) -> GraphState:
        print(Fore.YELLOW + "严格审核回复中，一丝不苟~...\n" + Style.RESET_ALL)
        is_rewrite = self.agents.verify_reply.invoke({"reply": state.generated_reply})
        if state.trials >=3:

        return {"is_rewrite": is_rewrite}

    # 审核咨询回复
    def verify_consultation_reply(self, state: GraphState) -> GraphState:
        print(Fore.YELLOW + "严格审核回复中，一丝不苟~...\n" + Style.RESET_ALL)
        is_rewrite = self.agents.verify_reply.invoke({"reply": state.generated_reply})

        return {"is_rewrite": is_rewrite}

   #结束节点
    def end(self, state: GraphState) -> GraphState:


        return