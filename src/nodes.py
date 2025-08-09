from .agents import Agents
from .state import GraphState
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

         return {"reviews": reviews}

    def select_current_review(self,state: GraphState)-> GraphState:

        current_review = state["reviews"][0]
        print(Fore.YELLOW + "→ 处理中：" + Style.RESET_ALL + f" {current_review}\n")

        return{"current_review": current_review}



    #评论分类：1.好评 2.差评 3.咨询评论
    def categorize_review(self, state: GraphState) -> GraphState:
        # 从状态中依次获取评论

        print(Fore.YELLOW + "正在判断当前评论的分类...\n" + Style.RESET_ALL)
        # invoke方法传入评论到提示词中，让大模型分类
        result = self.agents.categorize_review.invoke({"current_review": state["current_review"]})
        # 打印日志：展示分类结果（洋红色文字）
        print(Fore.MAGENTA + f"评论分类: {result["category"]}" + Style.RESET_ALL)
        #返回值添加到state中
        return { "review_category": result["category"]  }

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
        reply=self.agents.write_reply.invoke({
            "current_review": state["current_review"],
            "review_category":state["review_category"]
        })
        trials = state.get('trials', 0) + 1
        print(Fore.MAGENTA + f"{reply['generated_reply']}" + Style.RESET_ALL)
        return {"generated_reply": reply["generated_reply"], "trials": trials}

    #差评回复
    def reply_negative_review(self, state: GraphState) -> GraphState:
        print(Fore.YELLOW + "牛马正含着泪在回复差评...\n" + Style.RESET_ALL)
        reply=self.agents.write_reply.invoke({
            "current_review": state["current_review"],
            "review_category":state["review_category"]
        })
        trials = state.get('trials', 0) + 1
        print(Fore.MAGENTA + f"{reply['generated_reply']}" + Style.RESET_ALL)
        return {"generated_reply": reply["generated_reply"], "trials": trials}

    #咨询回复结合RAG
    def reply_consultation_review(self, state: GraphState) -> GraphState:
        print(Fore.YELLOW + "俺正在翻书解决小主的疑问\n" + Style.RESET_ALL)
        reply=self.agents.write_reply.invoke({
            "current_review": state["current_review"],
            "review_category":state["review_category"]
        })
        #TODO:添加Agent写回复结合RAG向量数据库
        trials = state.get('trials', 0) + 1
        print(Fore.MAGENTA + f"{reply['generated_reply']}" + Style.RESET_ALL)
        return {"generated_reply": reply["generated_reply"], "trials": trials}

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
                "review_reply": {"review": state["current_review"], "reply": "无法生成，请人工回复"}
            }
        if is_rewrite:
            return {"is_rewrite": True}
        else:
            #保存评论和回复
            return {
                "is_rewrite": False,
                "review_reply": {"review": state["current_review"], "reply":state["generated_reply"]}
            }
    #判断评论列表是否为空来选择下一步方案
    def is_end(self, state: GraphState) -> GraphState:
        state["reviews"].pop(0)
        next_do_reviews = state["reviews"]
        if next_do_reviews:
            return{"reviews": next_do_reviews, "is_end": False}
        else:
            return {"reviews":next_do_reviews, "is_end": True}


   #结束节点
    def end(self, state: GraphState) -> GraphState:


        return;