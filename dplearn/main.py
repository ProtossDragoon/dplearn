from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from dplearn import models, quiz_data
from dplearn.database import SessionLocal, engine
from dplearn.routers import quiz, results

# 모델 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='Design Pattern Quiz Trainer')

# 정적 파일 마운트
app.mount('/static', StaticFiles(directory='dplearn/static'), name='static')

# 템플릿 설정
templates = Jinja2Templates(directory='dplearn/templates')

# 라우터 등록
app.include_router(quiz.router)
app.include_router(results.router)


@app.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.get('/quiz', response_class=HTMLResponse)
async def quiz_page(request: Request):
    return templates.TemplateResponse('quiz.html', {'request': request})


@app.get('/results/{session_id}', response_class=HTMLResponse)
async def results_page(request: Request, session_id: int):
    return templates.TemplateResponse(
        'results.html',
        {
            'request': request,
            'session_id': session_id,
        },
    )


# 초기 데이터 로드
@app.on_event('startup')
async def startup_event():
    # 직접 DB 세션 생성
    db = SessionLocal()
    try:
        # 디자인 패턴 데이터 로드
        for pattern_data in quiz_data.DESIGN_PATTERNS:
            # 이미 존재하는지 확인
            existing_pattern = (
                db.query(models.DesignPattern)
                .filter(
                    models.DesignPattern.name == pattern_data['name'],
                )
                .first()
            )

            if not existing_pattern:
                db_pattern = models.DesignPattern(**pattern_data)
                db.add(db_pattern)

        db.commit()

        # 퀴즈 문제 데이터 로드
        for question_data in quiz_data.QUIZ_QUESTIONS:
            # 간단하게 이미 존재하는지 확인 (패턴 ID로)
            existing_question = (
                db.query(models.QuizQuestion)
                .filter(
                    models.QuizQuestion.pattern_id == question_data['pattern_id'],
                )
                .first()
            )

            if not existing_question:
                db_question = models.QuizQuestion(**question_data)
                db.add(db_question)

        db.commit()
    finally:
        db.close()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('dplearn.main:app', host='0.0.0.0', port=8000, reload=True)
