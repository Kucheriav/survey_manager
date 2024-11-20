


###NEED REFACTOR

@database_session
def add_test_users(session):
    with open('test_users.json') as file:
        users = json.load(file)
    session.add_all([User(**user) for user in users])
    session.commit()
    session.close()

@database_session
def get_question_id_by_answer(session, answer):
    q_id = session.query(Question).filter(Question.right_answer == answer).one().id
    return q_id


@database_session
def add_test_questions(session):
    with open('test_questions.json', encoding='utf8') as file:
        data = json.load(file)
    questions = []
    answer_options = {}
    for el in data:
        if el['type'] != 'открытый':
            answer_options[el['right_answer']] = el['answer_options']
        question = Question(text=el['text'], right_answer=el['right_answer'], type=el['type'])
        session.add(question)
        session.flush()
    session.commit()

    for key in answer_options:
        q_id = get_question_id_by_answer(key)
        print(q_id)
        for option in answer_options[key]:
            session.add(AnswerOption(text=option, question_id=q_id))
    session.commit()
    # session.close()