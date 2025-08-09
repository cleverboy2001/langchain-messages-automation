from colorama import Fore, Style
from src.graph import Workflow
from dotenv import load_dotenv
from typing import List

# Load all env variables
load_dotenv()

# config
config = {'recursion_limit': 100}

workflow = Workflow()
app = workflow.app

initial_state = {
    "reviews": [],
    "current_review": "",
    "review_category": "",
    "is_rewrite": False,
    "review_reply": List[dict],
    "generated_reply": "",
    "is_end": bool,
    "trials": 0
}

# Run the automation
print(Fore.GREEN + "开始自动回复评论..." + Style.RESET_ALL)
for output in app.stream(initial_state, config):
    for key, value in output.items():
        print(Fore.CYAN + f"{key}节点运行结束" + Style.RESET_ALL)


