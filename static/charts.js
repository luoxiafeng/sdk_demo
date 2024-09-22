/*
 * @Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
 * @Date: 2024-09-22 21:26:11
 * @LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
 * @LastEditTime: 2024-09-22 21:26:49
 * @FilePath: \sdk_demo\static\charts.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
document.addEventListener("DOMContentLoaded", function() {
    const chartData = {{ chart_data|tojson }};

    // Chip temperature chart
    const ctxChipTemp = document.getElementById('chipTempChart').getContext('2d');
    new Chart(ctxChipTemp, {
        type: 'line',
        data: {
            labels: chartData.timestamps,
            datasets: [{
                label: '芯片温度 (C)',
                data: chartData.chip_temp,
                borderColor: 'rgba(255, 99, 132, 1)',
                fill: false
            }]
        }
    });

    // CPU Usage chart
    const ctxCpu = document.getElementById('cpuUsageChart').getContext('2d');
    new Chart(ctxCpu, {
        type: 'line',
        data: {
            labels: chartData.timestamps,
            datasets: [{
                label: 'CPU 内存使用率 (%)',
                data: chartData.cpu_usage,
                borderColor: 'rgba(54, 162, 235, 1)',
                fill: false
            }]
        }
    });

    // TPU Usage chart
    const ctxTpu = document.getElementById('tpuUsageChart').getContext('2d');
    new Chart(ctxTpu, {
        type: 'line',
        data: {
            labels: chartData.timestamps,
            datasets: [{
                label: 'TPU 使用率 (%)',
                data: chartData.tpu_usage,
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false
            }]
        }
    });
});
