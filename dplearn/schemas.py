from datetime import datetime

from pydantic import BaseModel


class DesignPatternBase(BaseModel):
    name: str
    description: str


class DesignPatternCreate(DesignPatternBase):
    pass


class DesignPattern(DesignPatternBase):
    id: int

    class Config:
        from_attributes = True


class QuizQuestionBase(BaseModel):
    pattern_id: int
    code_example: str


class QuizQuestionCreate(QuizQuestionBase):
    pass


class QuizQuestion(QuizQuestionBase):
    id: int

    class Config:
        from_attributes = True


class QuizQuestionWithChoices(BaseModel):
    id: int
    code_example: str
    choices: list[DesignPattern]

    class Config:
        from_attributes = True


class QuizSessionBase(BaseModel):
    pass


class QuizSessionCreate(QuizSessionBase):
    pass


class QuizSession(QuizSessionBase):
    id: int
    start_time: datetime
    end_time: datetime | None = None
    total_score: int
    problems_solved: int
    correct_answers: int

    class Config:
        from_attributes = True


class QuizAnswerBase(BaseModel):
    session_id: int
    question_id: int
    selected_pattern_id: int
    time_taken: float


class QuizAnswerCreate(QuizAnswerBase):
    pass


class QuizAnswer(QuizAnswerBase):
    id: int
    is_correct: bool
    answered_at: datetime

    class Config:
        from_attributes = True


class QuizAnswerWithDetails(QuizAnswer):
    question: QuizQuestion
    selected_pattern: DesignPattern

    class Config:
        from_attributes = True


class QuizResult(BaseModel):
    session: QuizSession
    answers: list[QuizAnswerWithDetails]

    class Config:
        from_attributes = True


class DailyScore(BaseModel):
    date: str
    score: int
