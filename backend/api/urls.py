from django.urls import path
from . import views

urlpatterns = [
    path('auth/login/', views.login_view, name='login'),
    path('upload/', views.upload_csv, name='upload-csv'),
    path('data/', views.get_data, name='get-data'),
    path('summary/', views.get_summary, name='get-summary'),
    path('history/', views.get_history, name='get-history'),
    path('report/', views.generate_report, name='generate-report'),
]
