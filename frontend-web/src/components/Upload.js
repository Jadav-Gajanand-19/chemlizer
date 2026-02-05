import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import apiService from '../services/api';
import './Upload.css';

const Upload = ({ onUploadSuccess }) => {
    const [uploading, setUploading] = useState(false);
    const [progress, setProgress] = useState(0);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const onDrop = useCallback(async (acceptedFiles) => {
        if (acceptedFiles.length === 0) return;

        const file = acceptedFiles[0];

        // Validate file type
        if (!file.name.endsWith('.csv')) {
            setError('Please upload a CSV file');
            return;
        }

        setError('');
        setSuccess('');
        setUploading(true);
        setProgress(0);

        // Simulate progress
        const progressInterval = setInterval(() => {
            setProgress((prev) => {
                if (prev >= 90) {
                    clearInterval(progressInterval);
                    return 90;
                }
                return prev + 10;
            });
        }, 200);

        try {
            const response = await apiService.uploadCSV(file);
            clearInterval(progressInterval);
            setProgress(100);
            setSuccess(`Successfully uploaded ${file.name} with ${response.summary.total_count} records!`);

            setTimeout(() => {
                if (onUploadSuccess) onUploadSuccess(response);
            }, 1000);
        } catch (err) {
            clearInterval(progressInterval);
            setError(err.response?.data?.error || 'Upload failed. Please try again.');
            setProgress(0);
        } finally {
            setUploading(false);
        }
    }, [onUploadSuccess]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'text/csv': ['.csv']
        },
        multiple: false,
    });

    return (
        <div className="upload-container">
            <h2>Upload Equipment Data</h2>
            <p className="upload-subtitle">Upload a CSV file with equipment parameters</p>

            <div
                {...getRootProps()}
                className={`dropzone ${isDragActive ? 'active' : ''} ${uploading ? 'uploading' : ''}`}
            >
                <input {...getInputProps()} />

                <div className="dropzone-content">
                    <svg className="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>

                    {uploading ? (
                        <div className="uploading-state">
                            <p className="primary-text">Uploading...</p>
                            <div className="progress-bar">
                                <div className="progress-fill" style={{ width: `${progress}%` }}></div>
                            </div>
                            <p className="progress-text">{progress}%</p>
                        </div>
                    ) : isDragActive ? (
                        <p className="primary-text">Drop the CSV file here</p>
                    ) : (
                        <>
                            <p className="primary-text">Drag & drop CSV file here</p>
                            <p className="secondary-text">or click to browse files</p>
                            <p className="hint-text">Supported format: .csv</p>
                        </>
                    )}
                </div>
            </div>

            {error && (
                <div className="message error-message fade-in">
                    <span>❌</span> {error}
                </div>
            )}

            {success && (
                <div className="message success-message fade-in">
                    <span>✅</span> {success}
                </div>
            )}

            <div className="csv-format-info">
                <h4>Required CSV Format:</h4>
                <code>Equipment Name, Type, Flowrate, Pressure, Temperature</code>
            </div>
        </div>
    );
};

export default Upload;
