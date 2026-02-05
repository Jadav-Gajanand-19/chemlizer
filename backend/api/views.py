from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import FileResponse
from django.db.models import Avg
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch

from .models import Equipment, UploadHistory
from .serializers import EquipmentSerializer, UploadHistorySerializer, CSVUploadSerializer
from .utils import (
    parse_csv_file,
    calculate_summary_statistics,
    save_equipment_data,
    cleanup_old_uploads
)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """
    User authentication endpoint
    Returns: Token for authenticated user
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        })
    
    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['POST'])
def upload_csv(request):
    """
    Upload CSV file and parse equipment data
    Returns: Uploaded data summary
    """
    serializer = CSVUploadSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    csv_file = serializer.validated_data['file']
    
    try:
        # Parse CSV
        df = parse_csv_file(csv_file)
        
        # Calculate summary statistics
        summary = calculate_summary_statistics(df)
        
        # Create upload history record
        upload_history = UploadHistory.objects.create(
            user=request.user,
            filename=csv_file.name,
            num_records=summary['total_count'],
            avg_flowrate=summary['avg_flowrate'],
            avg_pressure=summary['avg_pressure'],
            avg_temperature=summary['avg_temperature']
        )
        
        # Save equipment data
        save_equipment_data(df, upload_history)
        
        # Cleanup old uploads (keep only last 5)
        cleanup_old_uploads(request.user, keep_count=5)
        
        return Response({
            'message': 'File uploaded successfully',
            'upload_id': upload_history.id,
            'summary': summary
        }, status=status.HTTP_201_CREATED)
        
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'Error processing file: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_data(request):
    """
    Get all equipment data for the current user's latest upload
    Returns: List of equipment records
    """
    # Get user's latest upload
    latest_upload = UploadHistory.objects.filter(user=request.user).first()
    
    if not latest_upload:
        return Response({'data': []})
    
    equipment = Equipment.objects.filter(upload_session=latest_upload)
    serializer = EquipmentSerializer(equipment, many=True)
    
    return Response({'data': serializer.data})


@api_view(['GET'])
def get_summary(request):
    """
    Get summary statistics for current user's latest upload
    Returns: Summary statistics
    """
    latest_upload = UploadHistory.objects.filter(user=request.user).first()
    
    if not latest_upload:
        return Response({
            'message': 'No data available',
            'summary': None
        })
    
    equipment = Equipment.objects.filter(upload_session=latest_upload)
    
    # Calculate type distribution
    type_distribution = {}
    for equip_type in equipment.values_list('equipment_type', flat=True).distinct():
        count = equipment.filter(equipment_type=equip_type).count()
        type_distribution[equip_type] = count
    
    summary = {
        'total_count': equipment.count(),
        'avg_flowrate': round(latest_upload.avg_flowrate, 2) if latest_upload.avg_flowrate else 0,
        'avg_pressure': round(latest_upload.avg_pressure, 2) if latest_upload.avg_pressure else 0,
        'avg_temperature': round(latest_upload.avg_temperature, 2) if latest_upload.avg_temperature else 0,
        'type_distribution': type_distribution
    }
    
    return Response({'summary': summary})


@api_view(['GET'])
def get_history(request):
    """
    Get last 5 upload history records for current user
    Returns: List of upload history
    """
    history = UploadHistory.objects.filter(user=request.user)[:5]
    serializer = UploadHistorySerializer(history, many=True)
    
    return Response({'history': serializer.data})


@api_view(['GET'])
def generate_report(request):
    """
    Generate PDF report of equipment data
    Returns: PDF file
    """
    latest_upload = UploadHistory.objects.filter(user=request.user).first()
    
    if not latest_upload:
        return Response(
            {'error': 'No data available to generate report'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    equipment = Equipment.objects.filter(upload_session=latest_upload)
    
    # Create PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0A4D68'),
        spaceAfter=30,
    )
    
    # Title
    title = Paragraph("ChemLizer Equipment Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Summary
    summary_text = f"""
    <b>Upload Date:</b> {latest_upload.uploaded_at.strftime('%Y-%m-%d %H:%M')}<br/>
    <b>File:</b> {latest_upload.filename}<br/>
    <b>Total Records:</b> {latest_upload.num_records}<br/>
    <b>Average Flowrate:</b> {latest_upload.avg_flowrate:.2f}<br/>
    <b>Average Pressure:</b> {latest_upload.avg_pressure:.2f}<br/>
    <b>Average Temperature:</b> {latest_upload.avg_temperature:.2f}
    """
    summary_para = Paragraph(summary_text, styles['BodyText'])
    elements.append(summary_para)
    elements.append(Spacer(1, 0.3*inch))
    
    # Equipment table
    table_data = [['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
    for equip in equipment:
        table_data.append([
            equip.equipment_name,
            equip.equipment_type,
            f"{equip.flowrate:.2f}",
            f"{equip.pressure:.2f}",
            f"{equip.temperature:.2f}"
        ])
    
    # Create table
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0A4D68')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    return FileResponse(
        buffer,
        as_attachment=True,
        filename=f'chemlizer_report_{latest_upload.id}.pdf'
    )
