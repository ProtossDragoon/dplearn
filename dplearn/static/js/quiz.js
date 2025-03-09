document.addEventListener('DOMContentLoaded', function() {
    // 퀴즈 세션 시작
    initQuizSession();
});

// 전역 변수
let quizSession = null;
let currentQuestion = null;
let questionStartTime = null;
let problemCount = 0;
let timerInterval = null;
let remainingSeconds = 180; // 3분

async function initQuizSession() {
    try {
        // 퀴즈 세션 생성
        const response = await fetch('/api/quiz/sessions', {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error('Failed to create quiz session');
        }
        
        quizSession = await response.json();
        console.log('Quiz session created:', quizSession);
        
        // 타이머 시작
        startTimer();
        
        // 첫 문제 로드
        loadNextQuestion();
    } catch (error) {
        console.error('Error initializing quiz session:', error);
        alert('퀴즈 세션을 시작하는 중 오류가 발생했습니다.');
    }
}

async function loadNextQuestion() {
    try {
        // 로딩 영역 표시, 문제 영역 숨김
        document.getElementById('loading-area').classList.remove('is-hidden');
        document.getElementById('question-area').classList.add('is-hidden');
        
        // 랜덤 문제 가져오기
        const response = await fetch('/api/quiz/questions/random');
        
        if (!response.ok) {
            throw new Error('Failed to fetch question');
        }
        
        currentQuestion = await response.json();
        console.log('New question loaded:', currentQuestion);
        
        // 화면에 문제 표시
        displayQuestion(currentQuestion);
        
        // 문제 시작 시간 기록
        questionStartTime = new Date();
        
        // 로딩 영역 숨김, 문제 영역 표시
        document.getElementById('loading-area').classList.add('is-hidden');
        document.getElementById('question-area').classList.remove('is-hidden');
    } catch (error) {
        console.error('Error loading next question:', error);
        alert('문제를 불러오는 중 오류가 발생했습니다.');
    }
}

function displayQuestion(question) {
    // 코드 예제 표시
    const codeElement = document.getElementById('code-example');
    codeElement.textContent = question.code_example;
    hljs.highlightElement(codeElement);
    
    // 선택지 컨테이너 초기화
    const choicesContainer = document.getElementById('choices-container');
    choicesContainer.innerHTML = '';
    
    // 선택지 표시
    question.choices.forEach(pattern => {
        const column = document.createElement('div');
        column.className = 'column is-6';
        
        const button = document.createElement('button');
        button.className = 'button is-fullwidth choice-button';
        button.setAttribute('data-pattern-id', pattern.id);
        button.innerHTML = `
            <div>
                <p class="is-size-5 has-text-weight-bold">${pattern.name}</p>
                <p class="is-size-7 mt-2">${pattern.description}</p>
            </div>
        `;
        
        // 선택지 클릭 이벤트
        button.addEventListener('click', () => selectAnswer(pattern.id));
        
        column.appendChild(button);
        choicesContainer.appendChild(column);
    });
}

async function selectAnswer(patternId) {
    try {
        // 답변 시간 계산
        const timeTaken = (new Date() - questionStartTime) / 1000;
        
        // 답변 제출
        const response = await fetch('/api/quiz/answers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: quizSession.id,
                question_id: currentQuestion.id,
                selected_pattern_id: patternId,
                time_taken: timeTaken
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to submit answer');
        }
        
        const answer = await response.json();
        console.log('Answer submitted:', answer);
        
        // 문제 수 증가
        problemCount++;
        document.getElementById('problem-count').textContent = problemCount;
        
        // 다음 문제 로드
        loadNextQuestion();
    } catch (error) {
        console.error('Error selecting answer:', error);
        alert('답변을 제출하는 중 오류가 발생했습니다.');
    }
}

function startTimer() {
    // 타이머 표시 초기화
    updateTimerDisplay();
    
    // 타이머 interval 설정
    timerInterval = setInterval(() => {
        remainingSeconds--;
        
        // 타이머 표시 업데이트
        updateTimerDisplay();
        
        // 시간이 10초 이하면 경고 스타일 적용
        if (remainingSeconds <= 10) {
            document.getElementById('timer').classList.add('timer-warning');
        }
        
        // 시간이 다 되면 퀴즈 종료
        if (remainingSeconds <= 0) {
            clearInterval(timerInterval);
            endQuizSession();
        }
    }, 1000);
}

function updateTimerDisplay() {
    const minutes = Math.floor(remainingSeconds / 60);
    const seconds = remainingSeconds % 60;
    document.getElementById('timer').textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
}

async function endQuizSession() {
    try {
        // 퀴즈 세션 종료
        const response = await fetch(`/api/quiz/sessions/${quizSession.id}/end`, {
            method: 'PUT'
        });
        
        if (!response.ok) {
            throw new Error('Failed to end quiz session');
        }
        
        const endedSession = await response.json();
        console.log('Quiz session ended:', endedSession);
        
        // 결과 페이지로 이동
        window.location.href = `/results/${quizSession.id}`;
    } catch (error) {
        console.error('Error ending quiz session:', error);
        alert('퀴즈 세션을 종료하는 중 오류가 발생했습니다.');
    }
}