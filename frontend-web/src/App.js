import React, { useState } from 'react';
import Login from './components/Login';
import Upload from './components/Upload';
import DataTable from './components/DataTable';
import Charts from './components/Charts';
import Summary from './components/Summary';
import apiService from './services/api';
import './App.css';

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(apiService.isAuthenticated());
    const [activeTab, setActiveTab] = useState('upload');
    const [dataUploaded, setDataUploaded] = useState(false);

    const handleLoginSuccess = () => {
        setIsAuthenticated(true);
    };

    const handleLogout = () => {
        apiService.logout();
        setIsAuthenticated(false);
        setActiveTab('upload');
        setDataUploaded(false);
    };

    const handleUploadSuccess = () => {
        setDataUploaded(true);
        setActiveTab('data');
    };

    if (!isAuthenticated) {
        return <Login onLoginSuccess={handleLoginSuccess} />;
    }

    return (
        <div className="app">
            <nav className="navbar">
                <div className="navbar-content">
                    <div className="navbar-brand">
                        <h1>ChemLizer</h1>
                        <span className="brand-subtitle">Chemical Equipment Visualizer</span>
                    </div>
                    <div className="navbar-actions">
                        <span className="user-info">👤 {apiService.getUsername()}</span>
                        <button onClick={handleLogout} className="btn btn-outline logout-btn">
                            Logout
                        </button>
                    </div>
                </div>
            </nav>

            <div className="main-content">
                <div className="tabs">
                    <button
                        className={`tab ${activeTab === 'upload' ? 'active' : ''}`}
                        onClick={() => setActiveTab('upload')}
                    >
                        📤 Upload
                    </button>
                    <button
                        className={`tab ${activeTab === 'data' ? 'active' : ''}`}
                        onClick={() => setActiveTab('data')}
                        disabled={!dataUploaded}
                    >
                        📋 Data Table
                    </button>
                    <button
                        className={`tab ${activeTab === 'charts' ? 'active' : ''}`}
                        onClick={() => setActiveTab('charts')}
                        disabled={!dataUploaded}
                    >
                        📊 Charts
                    </button>
                    <button
                        className={`tab ${activeTab === 'summary' ? 'active' : ''}`}
                        onClick={() => setActiveTab('summary')}
                        disabled={!dataUploaded}
                    >
                        📈 Summary
                    </button>
                </div>

                <div className="tab-content">
                    {activeTab === 'upload' && <Upload onUploadSuccess={handleUploadSuccess} />}
                    {activeTab === 'data' && <DataTable />}
                    {activeTab === 'charts' && <Charts />}
                    {activeTab === 'summary' && <Summary />}
                </div>
            </div>

            <footer className="footer">
                <p>ChemLizer v1.0 - Intern Screening Task © 2026</p>
            </footer>
        </div>
    );
}

export default App;
