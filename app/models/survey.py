from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Survey(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    questions = relationship("Question", secondary='question_survey_association', back_populates="surveys")


class QuestionSurveyAssociation(Base):
    question_id = Column(Integer, ForeignKey('questions.id'), primary_key=True)
    survey_id = Column(Integer, ForeignKey('surveys.id'), primary_key=True)