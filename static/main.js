document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('sensorChart').getContext('2d');
    let chart;

    async function loadData() {
        const resp = await fetch('/api/data');
        const data = await resp.json();
        const labels = data.map(d => new Date(d.timestamp).toLocaleString());
        const values = data.map(d => d.value);

        if (chart) {
            chart.data.labels = labels;
            chart.data.datasets[0].data = values;
            chart.update();
        } else {
            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Sensor Value',
                        data: values,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        tension: 0.1
                    }]
                },
                options: {
                    scales: {
                        x: {
                            display: true,
                            title: { display: true, text: 'Time' }
                        },
                        y: {
                            display: true,
                            title: { display: true, text: 'Value' }
                        }
                    }
                }
            });
        }
    }

    loadData();
    setInterval(loadData, 60000);
});
