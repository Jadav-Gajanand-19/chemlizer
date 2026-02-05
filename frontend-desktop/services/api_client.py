"""
API Client for ChemLizer Desktop Application
Handles all communication with the Django backend
"""

import requests
import json

API_BASE_URL = 'http://localhost:8000/api'

class APIClient:
    def __init__(self):
        self.token = None
        self.username = None
    
    def login(self, username, password):
        """Authenticate user and store token"""
        try:
            response = requests.post(
                f'{API_BASE_URL}/auth/login/',
                json={'username': username, 'password': password}
            )
            response.raise_for_status()
            data = response.json()
            self.token = data['token']
            self.username = data['username']
            return True, "Login successful"
        except requests.exceptions.RequestException as e:
            return False, str(e)
    
    def _get_headers(self):
        """Get headers with authentication token"""
        headers = {}
        if self.token:
            headers['Authorization'] = f'Token {self.token}'
        return headers
    
    def upload_csv(self, file_path):
        """Upload CSV file"""
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    f'{API_BASE_URL}/upload/',
                    files=files,
                    headers=self._get_headers()
                )
                response.raise_for_status()
                return True, response.json()
        except Exception as e:
            return False, str(e)
    
    def get_data(self):
        """Get equipment data"""
        try:
            response = requests.get(
                f'{API_BASE_URL}/data/',
                headers=self._get_headers()
            )
            response.raise_for_status()
            return True, response.json()
        except Exception as e:
            return False, str(e)
    
    def get_summary(self):
        """Get summary statistics"""
        try:
            response = requests.get(
                f'{API_BASE_URL}/summary/',
                headers=self._get_headers()
            )
            response.raise_for_status()
            return True, response.json()
        except Exception as e:
            return False, str(e)
    
    def download_report(self, save_path):
        """Download PDF report"""
        try:
            response = requests.get(
                f'{API_BASE_URL}/report/',
                headers=self._get_headers(),
                stream=True
            )
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return True, "Report downloaded successfully"
        except Exception as e:
            return False, str(e)
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        return self.token is not None
