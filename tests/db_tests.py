from db.functions import *
import json

@database_session
def get_all_users(session):
    data = session.query(User).all()
    return data


@database_session
def get_all_questions(session):
    data = session.query(Question).all()
    return data

@database_session
def get_all_options(session):
    data = session.query(AnswerOption).all()
    return data

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


def primary_db_test():
    #try to connect and get some data
    recreate_db()
    add_test_users()
    add_test_questions()
    res = get_all_users()
    print(*res, sep='\n')
    print('-' * 100)
    res = get_all_questions()
    print(*res, sep='\n')
    print('-' * 100)
    res = get_all_options()
    print(*res, sep='\n')


if __name__ == '__main__':
    primary_db_test()
