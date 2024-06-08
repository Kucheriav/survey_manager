from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship



QUESTION_TYPE = ['открытый', 'один ответ', 'множественный ответ']
Base = declarative_base()

class BaseMixin:
    def __str__(self):
        res = []
        for attr in dir(self):
            if not attr.startswith('_') and attr not in ['metadata',  'registry']:
                x = getattr(self, attr)
                res.append(f'{attr}: {x}')
        return ' '.join(res)

    def __repr__(self):
        return self.__str__()



class AnswerOption(Base, BaseMixin):
    __tablename__ = 'answer_options'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    question_id = Column(Integer, ForeignKey('questions.id'))


class Question(Base, BaseMixin):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    right_answer = Column(String)
    type = Column(Enum(*QUESTION_TYPE, name='question_type_enum'))
    answer_options = relationship("AnswerOption")
    # survey_id = Column(Integer, ForeignKey('surveys.id'))
    # surveys = relationship("Survey", secondary="question_survey_association", back_populates="questions")

#
# class Survey(Base, BaseMixin):
#     __tablename__ = 'surveys'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#
#     questions = relationship("Question", secondary="question_survey_association", back_populates="surveys")
#
# class QuestionSurveyAssociation(Base):
#     __tablename__ = 'question_survey_association'
#
#     question_id = Column(Integer, ForeignKey('questions.id'), primary_key=True)
#     survey_id = Column(Integer, ForeignKey('surveys.id'), primary_key=True)

class User(Base, BaseMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String)
    name = Column(String)
    surname = Column(String)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    reg_date = Column(DateTime)
    last_visit = Column(DateTime)
    is_teacher = Column(Boolean)
    is_admin = Column(Boolean)



# class UserSurvey(Base, BaseMixin):
#     __tablename__ = 'user_surveys'
#
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     survey_id = Column(Integer, ForeignKey('surveys.id'))
#     completed = Column(Boolean, default=False)













