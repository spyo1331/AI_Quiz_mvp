from flask import Blueprint, render_template
import json
from flask_app.app_blueprints import state

quiz_results = Blueprint('quiz_results', __name__)

@quiz_results.route('/')
def show_results():
    selected_type = state['final_suggestion']
    with open('text_database/descs.json', 'r', encoding='utf-8') as file:
        type_desc = json.load(file)


    if selected_type in ['INTJ', 'ENTP', 'INTP', 'ENTJ']:
        return render_template("result_purple.html",
                               type=selected_type,
                               first_fn_desc=type_desc[selected_type]['first_fn']['desc'],
                               first_fn_name=type_desc[selected_type]['first_fn']['name'],
                               second_fn_desc=type_desc[selected_type]['second_fn']['desc'],
                               second_fn_name=type_desc[selected_type]['second_fn']['name'],
                               third_fn_desc=type_desc[selected_type]['third_fn']['desc'],
                               third_fn_name=type_desc[selected_type]['third_fn']['name'],
                                fourth_fn_desc=type_desc[selected_type]['fourth_fn']['desc'],
                               fourth_fn_name=type_desc[selected_type]['fourth_fn']['name'],
                               fifth_fn_desc=type_desc[selected_type]['fifth_fn']['desc'],
                               fifth_fn_name=type_desc[selected_type]['fifth_fn']['name'],
                               sixth_fn_desc=type_desc[selected_type]['sixth_fn']['desc'],
                               sixth_fn_name=type_desc[selected_type]['sixth_fn']['name'],
                               seventh_fn_desc=type_desc[selected_type]['seventh_fn']['desc'],
                               seventh_fn_name=type_desc[selected_type]['seventh_fn']['name'],
                               eighth_fn_desc=type_desc[selected_type]['eighth_fn']['desc'],
                               eighth_fn_name=type_desc[selected_type]['eighth_fn']['name'],
                               )
    elif selected_type in ['INFP', 'ENFP', 'ENFJ', 'INFJ']:
        return render_template("result_green.html",
                               type=selected_type,
                               first_fn_desc=type_desc[selected_type]['first_fn']['desc'],
                               first_fn_name=type_desc[selected_type]['first_fn']['name'],
                               second_fn_desc=type_desc[selected_type]['second_fn']['desc'],
                               second_fn_name=type_desc[selected_type]['second_fn']['name'],
                               third_fn_desc=type_desc[selected_type]['third_fn']['desc'],
                               third_fn_name=type_desc[selected_type]['third_fn']['name'],
                                fourth_fn_desc=type_desc[selected_type]['fourth_fn']['desc'],
                               fourth_fn_name=type_desc[selected_type]['fourth_fn']['name'],
                               fifth_fn_desc=type_desc[selected_type]['fifth_fn']['desc'],
                               fifth_fn_name=type_desc[selected_type]['fifth_fn']['name'],
                               sixth_fn_desc=type_desc[selected_type]['sixth_fn']['desc'],
                               sixth_fn_name=type_desc[selected_type]['sixth_fn']['name'],
                               seventh_fn_desc=type_desc[selected_type]['seventh_fn']['desc'],
                               seventh_fn_name=type_desc[selected_type]['seventh_fn']['name'],
                               eighth_fn_desc=type_desc[selected_type]['eighth_fn']['desc'],
                               eighth_fn_name=type_desc[selected_type]['eighth_fn']['name'])

    elif selected_type in ['ISFP', 'ESTJ', 'ESFJ', 'ISTP']:
        return render_template("result_blue.html",
                               type=selected_type,
                               first_fn_desc=type_desc[selected_type]['first_fn']['desc'],
                               first_fn_name=type_desc[selected_type]['first_fn']['name'],
                               second_fn_desc=type_desc[selected_type]['second_fn']['desc'],
                               second_fn_name=type_desc[selected_type]['second_fn']['name'],
                               third_fn_desc=type_desc[selected_type]['third_fn']['desc'],
                               third_fn_name=type_desc[selected_type]['third_fn']['name'],
                                fourth_fn_desc=type_desc[selected_type]['fourth_fn']['desc'],
                               fourth_fn_name=type_desc[selected_type]['fourth_fn']['name'],
                               fifth_fn_desc=type_desc[selected_type]['fifth_fn']['desc'],
                               fifth_fn_name=type_desc[selected_type]['fifth_fn']['name'],
                               sixth_fn_desc=type_desc[selected_type]['sixth_fn']['desc'],
                               sixth_fn_name=type_desc[selected_type]['sixth_fn']['name'],
                               seventh_fn_desc=type_desc[selected_type]['seventh_fn']['desc'],
                               seventh_fn_name=type_desc[selected_type]['seventh_fn']['name'],
                               eighth_fn_desc=type_desc[selected_type]['eighth_fn']['desc'],
                               eighth_fn_name=type_desc[selected_type]['eighth_fn']['name'])

    elif selected_type in ['ESFP', 'ISFJ', 'ISTJ', 'ESTP']:
        return render_template("result_red.html",
                               type=selected_type,
                               first_fn_desc=type_desc[selected_type]['first_fn']['desc'],
                               first_fn_name=type_desc[selected_type]['first_fn']['name'],
                               second_fn_desc=type_desc[selected_type]['second_fn']['desc'],
                               second_fn_name=type_desc[selected_type]['second_fn']['name'],
                               third_fn_desc=type_desc[selected_type]['third_fn']['desc'],
                               third_fn_name=type_desc[selected_type]['third_fn']['name'],
                                fourth_fn_desc=type_desc[selected_type]['fourth_fn']['desc'],
                               fourth_fn_name=type_desc[selected_type]['fourth_fn']['name'],
                               fifth_fn_desc=type_desc[selected_type]['fifth_fn']['desc'],
                               fifth_fn_name=type_desc[selected_type]['fifth_fn']['name'],
                               sixth_fn_desc=type_desc[selected_type]['sixth_fn']['desc'],
                               sixth_fn_name=type_desc[selected_type]['sixth_fn']['name'],
                               seventh_fn_desc=type_desc[selected_type]['seventh_fn']['desc'],
                               seventh_fn_name=type_desc[selected_type]['seventh_fn']['name'],
                               eighth_fn_desc=type_desc[selected_type]['eighth_fn']['desc'],
                               eighth_fn_name=type_desc[selected_type]['eighth_fn']['name'])

    else: return render_template("parsing_error.html", error_parsed_text=state['final_suggestion'])