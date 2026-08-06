from flask import request, render_template, Blueprint, redirect, url_for
from flask_app.utils.graph import questions_config,  build_graph
from flask_app.app_blueprints import state
from langchain_core.messages import SystemMessage, HumanMessage

quiz = Blueprint('quiz', __name__)

graph = build_graph()


@quiz.route('/', methods=['GET', 'POST'])
def graph_fn():
    question_index = state['questions_asked']

    if request.method == 'GET':
        if question_index == 0 and len(state['messages']) == 0:
            state['messages'].append(SystemMessage(content=state['questions'][0]))

    else:
        user_answer = request.form.get('answer_place', '').strip()
        state['messages'].append(HumanMessage(content=user_answer))
        state['answers'].append(user_answer)
        state['questions_asked'] += 1
        question_index = state['questions_asked']

        if question_index < len(state['questions']):
            state['messages'].append(SystemMessage(content=state['questions'][question_index]))



    current_q = state['questions_asked']

    if current_q > 0 and current_q % questions_config.note_every_n_step == 0 and current_q < questions_config.max_questions_asked_limit:
        result = graph.invoke(state)
        state['intermediate_results'] = result.get('intermediate_results')


    elif current_q >= questions_config.max_questions_asked_limit:
        result = graph.invoke(state)
        state['intermediate_results'] = result.get('intermediate_results')
        state['explanation'] = result.get('explanation')
        state['final_suggestion'] = result.get('final_suggestion')
        return redirect(url_for('results.show_results'))


    finished = state['questions_asked'] >= len(state['questions'])
    current_question = None
    if not finished:
        current_question = state['questions'][state['questions_asked']]


    return render_template(
        'app1.html',
        questions=state['questions'],
        current_question=current_question,
        answers=state['answers'],
        finished=False,
        note_step=questions_config.note_every_n_step,
        current=state['questions_asked'],
        total=len(state['questions'])
    )

