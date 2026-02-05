"""
ChemLizer Desktop App - Main Window
Complete hybrid desktop application for chemical equipment data visualization
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QPushButton, QLabel, QFileDialog, QTableWidget, QTableWidgetItem,
    QTabWidget, QMessageBox, QGroupBox, QProgressBar, QHeaderView
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os

from services.api_client import APIClient

class LoginDialog(QWidget):
    """Login dialog for user authentication"""
    login_successful = pyqtSignal()
    
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("ChemLizer - Login")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Logo
        title = QLabel("ChemLizer")
        title.setProperty("class", "title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Chemical Equipment Parameter Visualizer")
        subtitle.setProperty("class", "subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Username
        from PyQt5.QtWidgets import QLineEdit
        username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password")
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        
        # Login button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)
        
        self.setLayout(layout)
    
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password")
            return
        
        success, message = self.api_client.login(username, password)
        
        if success:
            self.login_successful.emit()
            self.close()
        else:
            QMessageBox.critical(self, "Login Failed", f"Login failed: {message}")


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.current_data = []
        self.current_summary = None
        
        # Load stylesheet
        self.load_stylesheet()
        
        # Show login dialog
        self.login_dialog = LoginDialog(self.api_client)
        self.login_dialog.login_successful.connect(self.on_login_success)
        self.login_dialog.show()
        
        self.init_ui()
    
    def load_stylesheet(self):
        """Load QSS stylesheet"""
        try:
            qss_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'styles.qss')
            with open(qss_path, 'r') as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error loading stylesheet: {e}")
    
    def init_ui(self):
        """Initialize main UI"""
        self.setWindowTitle("ChemLizer - Chemical Equipment Visualizer")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Header
        header = QWidget()
        header_layout = QHBoxLayout()
        header.setLayout(header_layout)
        
        title = QLabel("ChemLizer")
        title.setProperty("class", "title")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.user_label = QLabel("")
        header_layout.addWidget(self.user_label)
        
        logout_btn = QPushButton("Logout")
        logout_btn.setProperty("class", "secondary")
        logout_btn.clicked.connect(self.handle_logout)
        header_layout.addWidget(logout_btn)
        
        main_layout.addWidget(header)
        
        # Tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Create tabs
        self.create_upload_tab()
        self.create_data_tab()
        self.create_charts_tab()
        self.create_summary_tab()
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def create_upload_tab(self):
        """Create upload tab"""
        upload_widget = QWidget()
        layout = QVBoxLayout()
        upload_widget.setLayout(layout)
        
        # Title
        title = QLabel("Upload Equipment Data")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        subtitle = QLabel("Select a CSV file to upload")
        subtitle.setProperty("class", "subtitle")
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Upload button
        upload_btn = QPushButton("📁 Select CSV File")
        upload_btn.setFixedHeight(60)
        upload_btn.clicked.connect(self.handle_upload)
        layout.addWidget(upload_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # CSV format info
        info_group = QGroupBox("Required CSV Format")
        info_layout = QVBoxLayout()
        info_group.setLayout(info_layout)
        
        format_label = QLabel("Equipment Name, Type, Flowrate, Pressure, Temperature")
        format_label.setFont(QFont("Courier New", 10))
        info_layout.addWidget(format_label)
        
        layout.addWidget(info_group)
        
        layout.addStretch()
        
        self.tabs.addTab(upload_widget, "📤 Upload")
    
    def create_data_tab(self):
        """Create data table tab"""
        data_widget = QWidget()
        layout = QVBoxLayout()
        data_widget.setLayout(layout)
        
        # Title
        header = QHBoxLayout()
        title = QLabel("Equipment Data")
        title.setProperty("class", "title")
        header.addWidget(title)
        
        header.addStretch()
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_data)
        header.addWidget(refresh_btn)
        
        layout.addLayout(header)
        
        # Table
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels(['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.data_table.setAlternatingRowColors(True)
        layout.addWidget(self.data_table)
        
        self.tabs.addTab(data_widget, "📋 Data Table")
    
    def create_charts_tab(self):
        """Create charts tab"""
        charts_widget = QWidget()
        layout = QVBoxLayout()
        charts_widget.setLayout(layout)
        
        title = QLabel("Data Visualizations")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        # Canvas for matplotlib
        self.figure = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        refresh_btn = QPushButton("🔄 Refresh Charts")
        refresh_btn.clicked.connect(self.load_charts)
        layout.addWidget(refresh_btn)
        
        self.tabs.addTab(charts_widget, "📊 Charts")
    
    def create_summary_tab(self):
        """Create summary tab"""
        summary_widget = QWidget()
        layout = QVBoxLayout()
        summary_widget.setLayout(layout)
        
        # Title
        header = QHBoxLayout()
        title = QLabel("Summary Statistics")
        title.setProperty("class", "title")
        header.addWidget(title)
        
        header.addStretch()
        
        download_btn = QPushButton("📄 Download PDF Report")
        download_btn.clicked.connect(self.download_report)
        header.addWidget(download_btn)
        
        layout.addLayout(header)
        
        # Summary labels
        self.summary_layout = QVBoxLayout()
        layout.addLayout(self.summary_layout)
        
        layout.addStretch()
        
        self.tabs.addTab(summary_widget, "📈 Summary")
    
    def on_login_success(self):
        """Handle successful login"""
        self.user_label.setText(f"👤 {self.api_client.username}")
        self.statusBar().showMessage(f"Logged in as {self.api_client.username}")
        self.show()
    
    def handle_logout(self):
        """Handle logout"""
        self.api_client.token = None
        self.api_client.username = None
        self.hide()
        self.login_dialog = LoginDialog(self.api_client)
        self.login_dialog.login_successful.connect(self.on_login_success)
        self.login_dialog.show()
    
    def handle_upload(self):
        """Handle CSV file upload"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if not file_path:
            return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.statusBar().showMessage("Uploading...")
        
        success, result = self.api_client.upload_csv(file_path)
        
        self.progress_bar.setVisible(False)
        
        if success:
            QMessageBox.information(
                self,
                "Success",
                f"File uploaded successfully!\n{result['summary']['total_count']} records imported."
            )
            self.statusBar().showMessage("Upload successful")
            self.load_data()
            self.load_charts()
            self.load_summary()
        else:
            QMessageBox.critical(self, "Error", f"Upload failed: {result}")
            self.statusBar().showMessage("Upload failed")
    
    def load_data(self):
        """Load equipment data into table"""
        success, result = self.api_client.get_data()
        
        if success:
            data = result.get('data', [])
            self.current_data = data
            
            self.data_table.setRowCount(len(data))
            
            for row, item in enumerate(data):
                self.data_table.setItem(row, 0, QTableWidgetItem(item['equipment_name']))
                self.data_table.setItem(row, 1, QTableWidgetItem(item['equipment_type']))
                self.data_table.setItem(row, 2, QTableWidgetItem(f"{item['flowrate']:.2f}"))
                self.data_table.setItem(row, 3, QTableWidgetItem(f"{item['pressure']:.2f}"))
                self.data_table.setItem(row, 4, QTableWidgetItem(f"{item['temperature']:.2f}"))
            
            self.statusBar().showMessage(f"Loaded {len(data)} records")
        else:
            QMessageBox.warning(self, "Error", f"Failed to load data: {result}")
    
    def load_charts(self):
        """Load and display charts"""
        success, result = self.api_client.get_summary()
        
        if not success:
            QMessageBox.warning(self, "Error", "Failed to load data for charts")
            return
        
        summary = result.get('summary', {})
        type_dist = summary.get('type_distribution', {})
        
        if not type_dist:
            return
        
        self.figure.clear()
        
        # Create 3 subplots
        ax1 = self.figure.add_subplot(2, 2, 1)
        ax2 = self.figure.add_subplot(2, 2, 2)
        ax3 = self.figure.add_subplot(2, 2, 3)
        
        # ChemLizer colors
        colors = ['#0A4D68', '#088395', '#05BFDB', '#FF6B6B', '#4ECDC4']
        
        # Bar chart - Equipment Type Distribution
        types = list(type_dist.keys())
        counts = list(type_dist.values())
        ax1.bar(types, counts, color='#05BFDB')
        ax1.set_title('Equipment Type Distribution', fontweight='bold', color='#0A4D68')
        ax1.set_xlabel('Equipment Type')
        ax1.set_ylabel('Count')
        ax1.tick_params(axis='x', rotation=45)
        
        # Pie chart - Type Distribution
        ax2.pie(counts, labels=types, autopct='%1.1f%%', colors=colors[:len(types)])
        ax2.set_title('Type Distribution', fontweight='bold', color='#0A4D68')
        
        # Bar chart - Average Parameters
        params = ['Avg Flowrate', 'Avg Pressure', 'Avg Temperature']
        values = [
            summary.get('avg_flowrate', 0),
            summary.get('avg_pressure', 0),
            summary.get('avg_temperature', 0)
        ]
        ax3.bar(params, values, color=['#0A4D68', '#088395', '#05BFDB'])
        ax3.set_title('Average Parameters', fontweight='bold', color='#0A4D68')
        ax3.tick_params(axis='x', rotation=45)
        
        self.figure.tight_layout()
        self.canvas.draw()
        
        self.statusBar().showMessage("Charts loaded")
    
    def load_summary(self):
        """Load summary statistics"""
        success, result = self.api_client.get_summary()
        
        if success:
            summary = result.get('summary', {})
            self.current_summary = summary
            
            # Clear existing summary
            while self.summary_layout.count():
                child = self.summary_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            
            # Add summary stats
            stats_group = QGroupBox("Overall Statistics")
            stats_layout = QVBoxLayout()
            stats_group.setLayout(stats_layout)
            
            stats_layout.addWidget(QLabel(f"📊 Total Equipment: {summary.get('total_count', 0)}"))
            stats_layout.addWidget(QLabel(f"💧 Average Flowrate: {summary.get('avg_flowrate', 0):.2f}"))
            stats_layout.addWidget(QLabel(f"⚡ Average Pressure: {summary.get('avg_pressure', 0):.2f}"))
            stats_layout.addWidget(QLabel(f"🌡️ Average Temperature: {summary.get('avg_temperature', 0):.2f}"))
            
            self.summary_layout.addWidget(stats_group)
            
            # Type distribution
            type_group = QGroupBox("Equipment Type Distribution")
            type_layout = QVBoxLayout()
            type_group.setLayout(type_layout)
            
            for eq_type, count in summary.get('type_distribution', {}).items():
                type_layout.addWidget(QLabel(f"{eq_type}: {count} units"))
            
            self.summary_layout.addWidget(type_group)
            
            self.statusBar().showMessage("Summary loaded")
    
    def download_report(self):
        """Download PDF report"""
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            f"chemlizer_report_{self.api_client.username}.pdf",
            "PDF Files (*.pdf)"
        )
        
        if not save_path:
            return
        
        self.statusBar().showMessage("Downloading report...")
        
        success, message = self.api_client.download_report(save_path)
        
        if success:
            QMessageBox.information(self, "Success", f"Report saved to: {save_path}")
            self.statusBar().showMessage("Report downloaded")
        else:
            QMessageBox.critical(self, "Error", f"Failed to download report: {message}")
            self.statusBar().showMessage("Download failed")
