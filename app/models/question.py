from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class AnswerMatchingEnum(Enum):
    FULL_MATCH = 'ПОЛНОЕ СОВПАДЕНИЕ'
    CONTAINTS_TEXT = 'СОДЕРЖИТ ТЕКСТ'


class Question(Base):
    id = Column(Integer, primary_key=True)
    text = Column(String, unique=True)
    answer_type = Column(PgEnum(AnswerMatchingEnum), nullable=False, default=AnswerMatchingEnum.CONTAINTS_TEXT)
    right_answer = Column(String)
    surveys = relationship("Survey", secondary='question_survey_association', back_populates="questions")

    def __str__(self):
        return f'''{self.text}\n{self.answer}'''
