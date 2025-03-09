import random
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dplearn import models, schemas
from dplearn.database import get_db

router = APIRouter(
    prefix='/api/quiz',
    tags=['quiz'],
)


@router.post('/sessions', response_model=schemas.QuizSession)
def create_quiz_session(db: Session = Depends(get_db)):
    """새 퀴즈 세션 생성"""
    db_session = models.QuizSession()
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


@router.get('/questions/random', response_model=schemas.QuizQuestionWithChoices)
def get_random_question(db: Session = Depends(get_db)):
    """랜덤 문제 가져오기"""
    # 전체 문제 수 확인
    total_questions = db.query(models.QuizQuestion).count()
    if total_questions == 0:
        raise HTTPException(status_code=404, detail='No questions available')

    # 랜덤 문제 선택
    random_offset = random.randint(0, total_questions - 1)
    question = db.query(models.QuizQuestion).offset(random_offset).first()

    # 선택지 생성 (정답 + 3개의 오답)
    all_patterns = db.query(models.DesignPattern).all()
    correct_pattern = (
        db.query(models.DesignPattern).filter(models.DesignPattern.id == question.pattern_id).first()
    )

    # 정답을 제외한 패턴들
    other_patterns = [p for p in all_patterns if p.id != correct_pattern.id]
    # 랜덤하게 3개 선택
    selected_patterns = random.sample(other_patterns, min(3, len(other_patterns)))
    # 정답 추가
    choices = selected_patterns + [correct_pattern]
    # 선택지 섞기
    random.shuffle(choices)

    return schemas.QuizQuestionWithChoices(
        id=question.id,
        code_example=question.code_example,
        choices=choices,
    )


@router.post('/answers', response_model=schemas.QuizAnswer)
def submit_answer(answer: schemas.QuizAnswerCreate, db: Session = Depends(get_db)):
    """퀴즈 답변 제출"""
    # 문제 확인
    question = db.query(models.QuizQuestion).filter(models.QuizQuestion.id == answer.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail='Question not found')

    # 세션 확인
    session = db.query(models.QuizSession).filter(models.QuizSession.id == answer.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail='Session not found')

    # 정답 확인
    is_correct = question.pattern_id == answer.selected_pattern_id

    # 답변 저장
    db_answer = models.QuizAnswer(
        session_id=answer.session_id,
        question_id=answer.question_id,
        selected_pattern_id=answer.selected_pattern_id,
        is_correct=is_correct,
        time_taken=answer.time_taken,
    )
    db.add(db_answer)

    # 세션 업데이트
    session.problems_solved += 1
    if is_correct:
        session.total_score += 1
        session.correct_answers += 1
    else:
        session.total_score -= 2

    db.commit()
    db.refresh(db_answer)
    return db_answer


@router.put('/sessions/{session_id}/end', response_model=schemas.QuizSession)
def end_quiz_session(session_id: int, db: Session = Depends(get_db)):
    """퀴즈 세션 종료"""
    session = db.query(models.QuizSession).filter(models.QuizSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail='Session not found')

    session.end_time = datetime.now()
    db.commit()
    db.refresh(session)
    return session
