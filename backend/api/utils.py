"""
Utility functions for CSV parsing and data analysis
"""
import pandas as pd
import io
from .models import Equipment, UploadHistory


def parse_csv_file(file_obj):
    """
    Parse uploaded CSV file and return pandas DataFrame
    
    Args:
        file_obj: Uploaded file object
        
    Returns:
        DataFrame with parsed CSV data
        
    Raises:
        ValueError: If CSV format is invalid
    """
    try:
        # Read CSV file
        df = pd.read_csv(file_obj)
        
        # Validate required columns
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
        
        # Check for empty dataframe
        if df.empty:
            raise ValueError("CSV file is empty")
        
        # Clean column names (remove extra spaces)
        df.columns = df.columns.str.strip()
        
        # Validate numeric columns
        numeric_columns = ['Flowrate', 'Pressure', 'Temperature']
        for col in numeric_columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                try:
                    df[col] = pd.to_numeric(df[col])
                except:
                    raise ValueError(f"Column '{col}' must contain numeric values")
        
        return df
        
    except pd.errors.EmptyDataError:
        raise ValueError("CSV file is empty")
    except pd.errors.ParserError:
        raise ValueError("Invalid CSV format")
    except Exception as e:
        raise ValueError(f"Error parsing CSV: {str(e)}")


def calculate_summary_statistics(df):
    """
    Calculate summary statistics from DataFrame
    
    Args:
        df: pandas DataFrame with equipment data
        
    Returns:
        Dictionary with summary statistics
    """
    summary = {
        'total_count': len(df),
        'avg_flowrate': round(df['Flowrate'].mean (), 2),
        'avg_pressure': round(df['Pressure'].mean(), 2),
        'avg_temperature': round(df['Temperature'].mean(), 2),
        'min_flowrate': round(df['Flowrate'].min(), 2),
        'max_flowrate': round(df['Flowrate'].max(), 2),
        'min_pressure': round(df['Pressure'].min(), 2),
        'max_pressure': round(df['Pressure'].max(), 2),
        'min_temperature': round(df['Temperature'].min(), 2),
        'max_temperature': round(df['Temperature'].max(), 2),
        'type_distribution': df['Type'].value_counts().to_dict()
    }
    
    return summary


def save_equipment_data(df, upload_history):
    """
    Save equipment data from DataFrame to database
    
    Args:
        df: pandas DataFrame with equipment data
        upload_history: UploadHistory instance
        
    Returns:
        Number of records saved
    """
    equipment_objects = []
    
    for _, row in df.iterrows():
        equipment = Equipment(
            upload_session=upload_history,
            equipment_name=row['Equipment Name'],
            equipment_type=row['Type'],
            flowrate=row['Flowrate'],
            pressure=row['Pressure'],
            temperature=row['Temperature']
        )
        equipment_objects.append(equipment)
    
    # Bulk create for better performance
    Equipment.objects.bulk_create(equipment_objects)
    
    return len(equipment_objects)


def cleanup_old_uploads(user, keep_count=5):
    """
    Delete old upload history records, keeping only the latest N
    
    Args:
        user: User instance
        keep_count: Number of recent uploads to keep (default: 5)
    """
    uploads = UploadHistory.objects.filter(user=user).order_by('-uploaded_at')
    
    if uploads.count() > keep_count:
        old_uploads = uploads[keep_count:]
        for upload in old_uploads:
            upload.delete()
