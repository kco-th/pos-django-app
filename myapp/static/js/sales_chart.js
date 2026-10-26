// static/js/sales_chart.js

function renderSalesChart(canvasId, labels, dataPoints) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    //JavaScript Chart.js library
    //ctx (Rendering Context):chart area
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Sales Revenue ($)',
                data: dataPoints,
                borderColor: '#1d4ed8',
                pointRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: true }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(235, 11, 11, 0.05)' }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}