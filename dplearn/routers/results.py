from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix='/api/results',
    tags=['results'],
)


@router.get('/sessions/{session_id}', response_model=schemas.QuizResult)
def get_session_result(session_id: int, db: Session = Depends(get_db)):
    """세션 결과 가져오기"""
    session = db.query(models.QuizSession).filter(models.QuizSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail='Session not found')

    answers = (
        db.query(models.QuizAnswer)
        .filter(
            models.QuizAnswer.session_id == session_id,
        )
        .all()
    )

    return schemas.QuizResult(
        session=session,
        answers=answers,
    )


@router.get('/daily-scores', response_model=list[schemas.DailyScore])
def get_daily_scores(db: Session = Depends(get_db)):
    """최근 30일간의 일별 점수 가져오기"""
    today = datetime.now().date()
    thirty_days_ago = today - timedelta(days=30)

    # 세션 종료된 것만 가져오기
    results = (
        db.query(
            func.date(models.QuizSession.end_time).label('date'),
            func.sum(models.QuizSession.total_score).label('score'),
        )
        .filter(
            models.QuizSession.end_time.isnot(None),
            func.date(models.QuizSession.end_time) >= thirty_days_ago,
        )
        .group_by(
            func.date(models.QuizSession.end_time),
        )
        .all()
    )

    # 결과를 dict로 변환
    results_dict = {str(date): score for date, score in results}

    # 30일치 데이터 준비 (빈 날짜는 0으로)
    daily_scores = []
    for i in range(30):
        date = today - timedelta(days=i)
        date_str = str(date)
        score = results_dict.get(date_str, 0)
        daily_scores.append(schemas.DailyScore(date=date_str, score=score))

    # 날짜 순으로 정렬
    daily_scores.sort(key=lambda x: x.date)

    return daily_scores
