from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from dplearn.database import Base


class QuizSession(Base):
    """퀴즈 세션 모델"""

    __tablename__ = 'quiz_sessions'

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, server_default=func.now())
    end_time = Column(DateTime, nullable=True)
    total_score = Column(Integer, default=0)
    problems_solved = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)

    answers = relationship('QuizAnswer', back_populates='session')


class DesignPattern(Base):
    """디자인 패턴 모델"""

    __tablename__ = 'design_patterns'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)

    questions = relationship('QuizQuestion', back_populates='pattern')


class QuizQuestion(Base):
    """퀴즈 문제 모델"""

    __tablename__ = 'quiz_questions'

    id = Column(Integer, primary_key=True, index=True)
    pattern_id = Column(Integer, ForeignKey('design_patterns.id'))
    code_example = Column(Text)
    scenario = Column(Text, nullable=True)  # 시나리오 설명 필드 추가

    pattern = relationship('DesignPattern', back_populates='questions')
    answers = relationship('QuizAnswer', back_populates='question')


class QuizAnswer(Base):
    """퀴즈 답변 모델"""

    __tablename__ = 'quiz_answers'

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey('quiz_sessions.id'))
    question_id = Column(Integer, ForeignKey('quiz_questions.id'))
    selected_pattern_id = Column(Integer, ForeignKey('design_patterns.id'), nullable=True)
    is_correct = Column(Boolean, default=False)
    time_taken = Column(Float)  # 문제 풀이에 소요된 시간(초)
    answered_at = Column(DateTime, server_default=func.now())

    session = relationship('QuizSession', back_populates='answers')
    question = relationship('QuizQuestion', back_populates='answers')
    selected_pattern = relationship('DesignPattern')
