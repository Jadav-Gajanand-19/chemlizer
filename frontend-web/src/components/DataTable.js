import React, { useState, useEffect } from 'react';
import apiService from '../services/api';
import './DataTable.css';

const DataTable = () => {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const response = await apiService.getData();
            setData(response.data || []);
        } catch (err) {
            console.error('Error fetching data:', err);
        } finally {
            setLoading(false);
        }
    };

    const requestSort = (key) => {
        let direction = 'asc';
        if (sortConfig.key === key && sortConfig.direction === 'asc') {
            direction = 'desc';
        }
        setSortConfig({ key, direction });

        const sorted = [...data].sort((a, b) => {
            if (a[key] < b[key]) return direction === 'asc' ? -1 : 1;
            if (a[key] > b[key]) return direction === 'asc' ? 1 : -1;
            return 0;
        });
        setData(sorted);
    };

    const getSortIcon = (key) => {
        if (sortConfig.key !== key) return '⇅';
        return sortConfig.direction === 'asc' ? '↑' : '↓';
    };

    if (loading) {
        return (
            <div className="data-table-container">
                <h2>Equipment Data</h2>
                <div className="skeleton-table">
                    {[...Array(5)].map((_, i) => (
                        <div key={i} className="skeleton-row skeleton"></div>
                    ))}
                </div>
            </div>
        );
    }

    if (data.length === 0) {
        return (
            <div className="data-table-container">
                <h2>Equipment Data</h2>
                <div className="empty-state">
                    <p>No data available. Please upload a CSV file.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="data-table-container">
            <div className="table-header">
                <h2>Equipment Data</h2>
                <span className="record-count">{data.length} records</span>
            </div>

            <div className="table-wrapper">
                <table className="data-table">
                    <thead>
                        <tr>
                            <th onClick={() => requestSort('equipment_name')}>
                                Equipment Name {getSortIcon('equipment_name')}
                            </th>
                            <th onClick={() => requestSort('equipment_type')}>
                                Type {getSortIcon('equipment_type')}
                            </th>
                            <th onClick={() => requestSort('flowrate')}>
                                Flowrate {getSortIcon('flowrate')}
                            </th>
                            <th onClick={() => requestSort('pressure')}>
                                Pressure {getSortIcon('pressure')}
                            </th>
                            <th onClick={() => requestSort('temperature')}>
                                Temperature {getSortIcon('temperature')}
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.map((item, index) => (
                            <tr key={item.id || index} className="fade-in" style={{ animationDelay: `${index * 0.02}s` }}>
                                <td className="equipment-name">{item.equipment_name}</td>
                                <td>
                                    <span className="type-badge">{item.equipment_type}</span>
                                </td>
                                <td className="numeric">{item.flowrate.toFixed(2)}</td>
                                <td className="numeric">{item.pressure.toFixed(2)}</td>
                                <td className="numeric">{item.temperature.toFixed(2)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default DataTable;
