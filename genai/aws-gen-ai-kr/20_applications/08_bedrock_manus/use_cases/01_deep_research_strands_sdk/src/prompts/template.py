import os
from datetime import datetime
from langchain_core.prompts import PromptTemplate
from langgraph.prebuilt.chat_agent_executor import AgentState

def get_prompt_template(prompt_name: str) -> str:
    template = open(os.path.join(os.path.dirname(__file__), f"{prompt_name}.md")).read()
    return template

def apply_prompt_template(prompt_name: str, state: AgentState) -> list:

    system_prompts = get_prompt_template(prompt_name)

    if prompt_name in ["planner"]:
        context = {
            "CURRENT_TIME": datetime.now().strftime("%a %b %d %Y %H:%M:%S %z"),
            "ORIGIANL_USER_REQUEST": state["request"],
            "FOLLOW_UP_QUESTIONS": state["follow_up_questions"],
            "USER_FEEDBACK": state["user_feedback"]
        }
    elif prompt_name in ["researcher", "coder", "reporter"]:
        context = {
            "CURRENT_TIME": datetime.now().strftime("%a %b %d %Y %H:%M:%S %z"),
            "USER_REQUEST": state["request"],
            "FULL_PLAN": state["full_plan"]
        }
    else: context = {"CURRENT_TIME": datetime.now().strftime("%a %b %d %Y %H:%M:%S %z")}

    system_prompts = system_prompts.format(**context)
    return system_prompts