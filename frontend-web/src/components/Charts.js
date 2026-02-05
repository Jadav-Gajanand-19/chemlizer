import React, { useState, useEffect } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    LineElement,
    ArcElement,
    PointElement,
    Title,
    Tooltip,
    Legend,
    Filler
} from 'chart.js';
import { Bar, Line, Doughnut } from 'react-chartjs-2';
import apiService from '../services/api';
import theme from '../theme';
import './Charts.css';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    LineElement,
    ArcElement,
    PointElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

const Charts = () => {
    const [summary, setSummary] = useState(null);
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const [summaryRes, dataRes] = await Promise.all([
                apiService.getSummary(),
                apiService.getData()
            ]);
            setSummary(summaryRes.summary);
            setData(dataRes.data || []);
        } catch (err) {
            console.error('Error fetching data:', err);
        } finally {
            setLoading(false);
        }
    };

    if (loading || !summary) {
        return <div className="charts-container">Loading charts...</div>;
    }

    // Type Distribution Bar Chart
    const typeLabels = Object.keys(summary.type_distribution || {});
    const typeCounts = Object.values(summary.type_distribution || {});

    const barData = {
        labels: typeLabels,
        datasets: [
            {
                label: 'Equipment Count',
                data: typeCounts,
                backgroundColor: theme.colors.accent,
                borderRadius: 8,
                borderWidth: 0,
            },
        ],
    };

    const barOptions = {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
            duration: 1000,
            easing: 'easeOutQuart',
            delay: (context) => context.dataIndex * 100,
        },
        plugins: {
            legend: {
                display: false,
            },
            title: {
                display: true,
                text: 'Equipment Type Distribution',
                font: { size: 16, weight: '600' },
                color: theme.colors.primary,
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: '#F0F0F0',
                },
            },
            x: {
                grid: {
                    display: false,
                },
            },
        },
    };

    // Parameter Trends Line Chart
    const parameterData = {
        labels: data.slice(0, 10).map((item, i) => `#${i + 1}`),
        datasets: [
            {
                label: 'Flowrate',
                data: data.slice(0, 10).map(item => item.flowrate),
                borderColor: theme.colors.primary,
                backgroundColor: `${theme.colors.primary}20`,
                tension: 0.4,
                fill: true,
            },
            {
                label: 'Pressure',
                data: data.slice(0, 10).map(item => item.pressure),
                borderColor: theme.colors.secondary,
                backgroundColor: `${theme.colors.secondary}20`,
                tension: 0.4,
                fill: true,
            },
            {
                label: 'Temperature',
                data: data.slice(0, 10).map(item => item.temperature),
                borderColor: theme.colors.accent,
                backgroundColor: `${theme.colors.accent}20`,
                tension: 0.4,
                fill: true,
            },
        ],
    };

    const lineOptions = {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
            duration: 1500,
            easing: 'easeInOutQuart',
        },
        plugins: {
            legend: {
                position: 'bottom',
            },
            title: {
                display: true,
                text: 'Parameter Trends (First 10 Items)',
                font: { size: 16, weight: '600' },
                color: theme.colors.primary,
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: '#F0F0F0',
                },
            },
            x: {
                grid: {
                    display: false,
                },
            },
        },
    };

    // Type Distribution Doughnut Chart
    const doughnutData = {
        labels: typeLabels,
        datasets: [
            {
                data: typeCounts,
                backgroundColor: [
                    theme.colors.primary,
                    theme.colors.secondary,
                    theme.colors.accent,
                    '#FF6B6B',
                    '#4ECDC4',
                    '#45B7D1',
                ],
                borderWidth: 0,
            },
        ],
    };

    const doughnutOptions = {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
            animateRotate: true,
            animateScale: true,
            duration: 1200,
        },
        plugins: {
            legend: {
                position: 'right',
            },
            title: {
                display: true,
                text: 'Type Distribution',
                font: { size: 16, weight: '600' },
                color: theme.colors.primary,
            },
        },
    };

    return (
        <div className="charts-container">
            <h2>Data Visualizations</h2>

            <div className="charts-grid">
                <div className="chart-card fade-in">
                    <div className="chart-wrapper">
                        <Bar data={barData} options={barOptions} />
                    </div>
                </div>

                <div className="chart-card fade-in" style={{ animationDelay: '0.1s' }}>
                    <div className="chart-wrapper">
                        <Line data={parameterData} options={lineOptions} />
                    </div>
                </div>

                <div className="chart-card fade-in" style={{ animationDelay: '0.2s' }}>
                    <div className="chart-wrapper">
                        <Doughnut data={doughnutData} options={doughnutOptions} />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Charts;
