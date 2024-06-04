from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    text = Column(String)
    answer = Column(String)

    survey_id = Column(Integer, ForeignKey('surveys.id'))
    surveys = relationship("Survey", secondary="question_survey_association", back_populates="questions")

class Survey(Base):
    __tablename__ = 'surveys'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    questions = relationship("Question", secondary="question_survey_association", back_populates="surveys")

class QuestionSurveyAssociation(Base):
    __tablename__ = 'question_survey_association'

    question_id = Column(Integer, ForeignKey('questions.id'), primary_key=True)
    survey_id = Column(Integer, ForeignKey('surveys.id'), primary_key=True)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String)
    name = Column(String)
    surname = Column(String)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    is_teacher = Column(Boolean)
    is_admin = Column(Boolean)


class UserSurvey(Base):
    __tablename__ = 'user_surveys'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    survey_id = Column(Integer, ForeignKey('surveys.id'))
    completed = Column(Boolean, default=False)

# Создаем базу данных и таблицы
engine = create_engine('sqlite:///survey.db')
Base.metadata.create_all(engine)












