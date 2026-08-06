import os
from typing import List
from langchain.agents import create_agent
from flask_app.utils.vdb_for_so import retriever_soc, retriever_soc_behav
from langchain_core.tools import create_retriever_tool
from pydantic import BaseModel, Field
from langgraph.graph import  StateGraph, START, END, add_messages
from typing import Literal, Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
import json



load_dotenv()
api_key = os.getenv('API_KEY')



llm = ChatDeepSeek(model='deepseek-v4-flash', api_key=api_key, temperature=0.35)
retriever_tool = create_retriever_tool(retriever=retriever_soc, name='RAG_16types', description='Ищет подходящий чанк информации про тип личности в базе знаний. Полезен для окончательного вывода.')
retriever_tool_for_behav = create_retriever_tool(retriever=retriever_soc_behav, name='RAG_16types_expose', description='Ищет общую информацию по всем типам, поможет отличить логика от этика, сенсорика от интуита и так далее, полезен для промежуточных результатов')


types = Literal['INTJ', 'ENTP', 'ISFP', 'ESFJ',
                'ISTJ', 'ESTP', 'INFP', 'ENFJ',
                'INTP', 'ENTJ', 'ISFJ', 'ESFP',
                'ISTP', 'ESTJ', 'INFJ', 'ENFP',
                'UNKNOWN']



class DescsConfig:
    max_questions_asked_limit: int =  8
    note_every_n_step: int = 4


questions_config = DescsConfig()



class EndAnalysis(BaseModel):
    final_suggestion: str = Field(..., description='После анализа используя базу данных сделай вывод о том какой тип личности пользователя. В ответе указать только тип личности и ничего больше.')





class State(TypedDict):
    messages: Annotated[list, add_messages]
    intermediate_results: str|None
    questions_asked: int
    questions: List[str]
    final_suggestion: str|None
    explanation: str|None







def intermed_analysis(state: State):
    all_messages = state['messages']


    agent = create_agent(model=llm, tools=[retriever_tool, retriever_tool_for_behav])

    response = agent.invoke({'messages': [
        {'role': 'system',
         'content': 'Ты русский специалист по соционике. Ты можешь использовать поиск по базе данных, возможно тебе придется использовать инструмент несколько раз. Сейчас тебе придется дать промежуточные результаты о типе личности пользователя от третьего лица и КРАТКО это обосновать, вопросов никаких задавать не надо, потому что ты будешь использовать свои заметки в будущем. Вопросы задает система и вопросы выбираются случайным путем.'
                    'ПРИМЕР: пользователь ответил, что не понимает как он обижает людей, значит твой фокус должен смениться на болевую этику отношений и поискать про нее в базе данных или пользователь ответил, что не выразителен по эмоциям и вообще не разговорчив, значит он предположительно будет интровертом логиком.'},
        *all_messages
    ]})

    return {"intermediate_results": response['messages'][-1].content}






def end_analysis(state: State):
    llm.temperature = 0.0
    all_messages = state['messages']
    notes = state['intermediate_results']

    system_prompt = f"""Твоя задача тут уже финально определить тип личности пользователя.\nВот заметки {notes}"""

    agent = create_agent(model=llm, tools=[retriever_tool, retriever_tool_for_behav])
    response = agent.invoke({"messages": [*all_messages, {"role": 'system', 'content': system_prompt}]})

    for_parse = response['messages'][-1]

    return {"explanation": for_parse.content}






def parse_type(state: State):
    llm.temperature=0.0
    test_results = state['explanation']
    system_prompt = """О каком типе личности из 16 идет речь? Твоим ответом будет только valid JSON: {"final_suggestion": "Тип личности (ENFP|INTJ|INFJ|ESTP... или UNKNOWN)"}"""

    response = llm.invoke([{'role': 'system', 'content': system_prompt},
                           {'role': 'user', 'content': test_results}], response_format={"type": "json_object"})

    data = json.loads(response.content)
    parsed_response = EndAnalysis(**data)

    return {"final_suggestion": parsed_response.final_suggestion}




def build_graph():
    gr = StateGraph(State)

    gr.add_node('in_an', intermed_analysis)
    gr.add_node('en_an', end_analysis)
    gr.add_node('parse', parse_type)

    # Условный вход: что запускать
    def route_start(state: State):
        asked = state['questions_asked']
        if asked >= questions_config.max_questions_asked_limit:
            return 'en_an'
        elif asked > 0 and asked % questions_config.note_every_n_step == 0:
            return 'in_an'
        else:
            return 'end'

    gr.add_conditional_edges(START, route_start, {
        'in_an': 'in_an',
        'en_an': 'en_an',
        'end': END
    })

    gr.add_edge('in_an', END)
    gr.add_edge('en_an', 'parse')
    gr.add_edge('parse', END)

    return gr.compile()










