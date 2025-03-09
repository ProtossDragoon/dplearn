document.addEventListener('DOMContentLoaded', function() {
    const startQuizBtn = document.getElementById('start-quiz');
    const scoreChartContainer = document.getElementById('score-chart');
    
    // 퀴즈 시작 버튼 클릭 이벤트
    startQuizBtn.addEventListener('click', function() {
        // 버튼 로딩 상태 표시
        startQuizBtn.classList.add('is-loading');
        
        // 새 퀴즈 세션 생성 API 호출
        fetch('http://localhost:8000/api/quiz/sessions/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            // 세션 ID를 로컬 스토리지에 저장
            localStorage.setItem('quiz_session_id', data.id);
            // 퀴즈 페이지로 이동
            window.location.href = 'quiz.html';
        })
        .catch(error => {
            console.error('Error starting quiz session:', error);
            
            // 버튼 로딩 상태 제거
            startQuizBtn.classList.remove('is-loading');
            
            // 에러 메시지 표시
            showNotification('퀴즈를 시작하는 중 오류가 발생했습니다.', 'is-danger');
        });
    });
    
    // 점수 차트 데이터 가져오기
    fetch('http://localhost:8000/api/quiz/score/summary')
        .then(response => response.json())
        .then(data => {
            renderScoreChart(data);
        })
        .catch(error => {
            console.error('Error fetching score summary:', error);
            scoreChartContainer.innerHTML = '<div class="notification is-warning has-text-centered">점수 데이터를 불러올 수 없습니다.</div>';
        });
    
    // 점수 차트 렌더링 함수
    function renderScoreChart(data) {
        if (data.length === 0) {
            scoreChartContainer.innerHTML = '<div class="notification is-info has-text-centered">최근 30일간 퀴즈 기록이 없습니다.</div>';
            return;
        }
        
        const dates = data.map(item => item.date);
        const scores = data.map(item => item.score);
        
        const ctx = document.createElement('canvas');
        scoreChartContainer.appendChild(ctx);
        
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: dates,
                datasets: [{
                    label: '일일 점수',
                    data: scores,
                    backgroundColor: '#00d1b2',
                    borderColor: '#00c4a7',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                }
            }
        });
    }
    
    // 알림 메시지 표시 함수
    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification ${type} is-light`;
        notification.innerHTML = `
            <button class="delete"></button>
            ${message}
        `;
        
        document.querySelector('.container').prepend(notification);
        
        // 삭제 버튼 이벤트
        notification.querySelector('.delete').addEventListener('click', function() {
            notification.remove();
        });
        
        // 5초 후 자동으로 사라짐
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
});
