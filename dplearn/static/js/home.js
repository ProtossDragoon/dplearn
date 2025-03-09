document.addEventListener('DOMContentLoaded', function() {
    // 최근 30일 점수 차트 로드
    loadScoreChart();
});

async function loadScoreChart() {
    try {
        // API에서 데이터 가져오기
        const response = await fetch('/api/results/daily-scores');
        if (!response.ok) {
            throw new Error('Failed to fetch daily scores');
        }
        
        const data = await response.json();
        
        // 데이터 포맷 변환
        const labels = data.map(item => formatDate(item.date));
        const scores = data.map(item => item.score);
        
        // 차트 생성
        const ctx = document.getElementById('scoreChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: '일별 점수',
                    data: scores,
                    backgroundColor: 'rgba(72, 199, 116, 0.2)',
                    borderColor: 'rgba(72, 199, 116, 1)',
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
                }
            }
        });
    } catch (error) {
        console.error('Error loading score chart:', error);
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return `${date.getMonth() + 1}/${date.getDate()}`;
}