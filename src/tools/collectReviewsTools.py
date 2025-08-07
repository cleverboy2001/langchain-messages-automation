from src.agents import Agents


class ReviewToolsClass:
    def __init__(self):
        #创建一个搜集网页评论的Agent
        #或者直接使用mcp工具获取网页评论信息
        self.agents = Agents()