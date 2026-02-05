import React, { useState, useEffect } from 'react';
import apiService from '../services/api';
import './Summary.css';

const Summary = () => {
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchSummary();
    }, []);

    const fetchSummary = async () => {
        try {
            const response = await apiService.getSummary();
            setSummary(response.summary);
        } catch (err) {
            console.error('Error fetching summary:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleDownloadReport = async () => {
        try {
            await apiService.downloadReport();
        } catch (err) {
            console.error('Error downloading report:', err);
            alert('Failed to download report');
        }
    };

    if (loading) {
        return (
            <div className="summary-container">
                <h2>Summary Statistics</h2>
                <div className="stats-grid">
                    {[...Array(6)].map((_, i) => (
                        <div key={i} className="stat-card skeleton"></div>
                    ))}
                </div>
            </div>
        );
    }

    if (!summary) {
        return (
            <div className="summary-container">
                <h2>Summary Statistics</h2>
                <div className="empty-state">
                    <p>No data available. Please upload a CSV file.</p>
                </div>
            </div>
        );
    }

    const stats = [
        { label: 'Total Equipment', value: summary.total_count, icon: '📊', color: '#0A4D68' },
        { label: 'Avg Flowrate', value: summary.avg_flowrate.toFixed(2), icon: '💧', color: '#088395' },
        { label: 'Avg Pressure', value: summary.avg_pressure.toFixed(2), icon: '⚡', color: '#05BFDB' },
        { label: 'Avg Temperature', value: summary.avg_temperature.toFixed(2), icon: '🌡️', color: '#FF6B6B' },
    ];

    return (
        <div className="summary-container">
            <div className="summary-header">
                <h2>Summary Statistics</h2>
                <button onClick={handleDownloadReport} className="btn btn-primary">
                    📄 Download PDF Report
                </button>
            </div>

            <div className="stats-grid">
                {stats.map((stat, index) => (
                    <div
                        key={stat.label}
                        className="stat-card fade-in"
                        style={{ animationDelay: `${index * 0.1}s` }}
                    >
                        <div className="stat-icon" style={{ background: `${stat.color}15`, color: stat.color }}>
                            {stat.icon}
                        </div>
                        <div className="stat-content">
                            <div className="stat-value" style={{ color: stat.color }}>
                                {stat.value}
                            </div>
                            <div className="stat-label">{stat.label}</div>
                        </div>
                    </div>
                ))}
            </div>

            <div className="type-distribution-section fade-in" style={{ animationDelay: '0.4s' }}>
                <h3>Equipment Type Distribution</h3>
                <div className="type-list">
                    {Object.entries(summary.type_distribution || {}).map(([type, count], index) => (
                        <div key={type} className="type-item" style={{ animationDelay: `${0.5 + index * 0.05}s` }}>
                            <div className="type-info">
                                <span className="type-name">{type}</span>
                                <span className="type-count">{count} units</span>
                            </div>
                            <div className="type-bar">
                                <div
                                    className="type-bar-fill"
                                    style={{
                                        width: `${(count / summary.total_count) * 100}%`,
                                        animationDelay: `${0.6 + index * 0.05}s`,
                                    }}
                                ></div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Summary;
