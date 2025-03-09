document.addEventListener('DOMContentLoaded', function() {
    // 결과 로드
    loadResults();
});

async function loadResults() {
    try {
        // 세션 결과 가져오기
        const response = await fetch(`/api/results/sessions/${sessionId}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch results');
        }
        
        const results = await response.json();
        console.log('Quiz results:', results);
        
        // 결과 요약 표시
        displayResultSummary(results.session);
        
        // 문제별 결과 표시
        displayAnswerDetails(results.answers);
    } catch (error) {
        console.error('Error loading results:', error);
        alert('결과를 불러오는 중 오류가 발생했습니다.');
    }
}

function displayResultSummary(session) {
    // 결과 요약 표시
    document.getElementById('total-score').textContent = session.total_score;
    document.getElementById('problems-solved').textContent = session.problems_solved;
    document.getElementById('correct-answers').textContent = session.correct_answers;
    
    // 정확도 계산 (0으로 나누기 방지)
    let accuracy = 0;
    if (session.problems_solved > 0) {
        accuracy = ((session.correct_answers / session.problems_solved) * 100).toFixed(1);
    }
    document.getElementById('accuracy').textContent = `${accuracy}%`;
}

function displayAnswerDetails(answers) {
    const answersTable = document.getElementById('answers-table');
    answersTable.innerHTML = '';
    
    if (answers.length === 0) {
        // 답변이 없는 경우
        const row = document.createElement('tr');
        row.innerHTML = `
            <td colspan="4" class="has-text-centered">답변이 없습니다.</td>
        `;
        answersTable.appendChild(row);
        return;
    }
    
    // 답변 순서대로 표시
    answers.forEach((answer, index) => {
        const row = document.createElement('tr');
        row.className = answer.is_correct ? 'is-correct' : 'is-incorrect';
        
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${answer.selected_pattern.name}</td>
            <td>
                <span class="${answer.is_correct ? 'correct' : 'incorrect'}">
                    <i class="fas fa-${answer.is_correct ? 'check' : 'times'}"></i>
                    ${answer.is_correct ? '정답' : '오답'}
                </span>
            </td>
            <td>${formatTime(answer.time_taken)}</td>
        `;
        
        answersTable.appendChild(row);
    });
}

function formatTime(seconds) {
    if (seconds < 60) {
        return `${seconds.toFixed(1)}초`;
    } else {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = (seconds % 60).toFixed(1);
        return `${minutes}분 ${remainingSeconds}초`;
    }
}