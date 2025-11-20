import requests
import csv
import json
import time
import openpyxl
from openpyxl import Workbook
from datetime import datetime
from zoneinfo import ZoneInfo
import os
from dotenv import load_dotenv

def fetch_data(endpoint, record_type):
    """
    Generic function to fetch data from API with pagination
    """
    load_dotenv()
    base_domain = os.getenv('DOMAIN_API')
    rest_api_key = os.getenv('REST_API_KEY')
    base_url = f'https://{base_domain}/api/odata/businessobject/{endpoint}'
    
    
    
    headers = {
        'Authorization': f'rest_api_key={rest_api_key}',
        'rest_api_key': rest_api_key
    }
    
    all_records = []
    skip = 0
    top = 100
    
    while True:
        url = f'{base_url}?$top={top}&$skip={skip}'
        print(f"Fetching {record_type} {skip} to {skip + top}...")
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        records = data.get('value', [])
        
        if not records:
            print(f"No more {record_type} to fetch")
            break
        
        all_records.extend(records)
        print(f"Retrieved {len(records)} {record_type}. Total: {len(all_records)}")
        
        if len(records) < top:
            break
        
        skip += top
        time.sleep(1)
    
    return all_records

def transform_records(records, tipo, number_field):
    """
    Transform records to common format
    """
    filtered_records = []
    fecha_hoy = datetime.now(ZoneInfo("America/Bogota")).strftime('%Y-%m-%d %H:%M:%S')
    
    for record in records:
        fecha_creacion_raw = record.get('CreatedDateTime', '')
        fecha_creacion_formatted = ''
        hora_creacion_formatted = ''
        if fecha_creacion_raw:
            try:
                dt = datetime.fromisoformat(fecha_creacion_raw.replace('Z', '+00:00'))
                dt_bogota = dt.astimezone(ZoneInfo("America/Bogota"))
                fecha_creacion_formatted = dt_bogota.strftime('%Y-%m-%d')
                hora_creacion_formatted = dt_bogota.strftime('%H:%M:%S')
            except:
                fecha_creacion_formatted = fecha_creacion_raw
                hora_creacion_formatted = ''
        
        filtered_record = {
            'Owner': record.get('Owner', ''),
            'fecha_hoy': fecha_hoy,
            'tipo': tipo,
            'fecha_creacion': fecha_creacion_formatted,
            'hora_creacion': hora_creacion_formatted,
            'idticket': record.get(number_field, ''),
            'asunto': record.get('Subject', ''),
            'estado': record.get('Status', '')
        }
        filtered_records.append(filtered_record)
    
    return filtered_records

def fetch_incidents_and_servicereqs():
    """
    Fetch incidents and service requests from the API and save as combined CSV/XLSX files
    """
    try:
        # Fetch incidents
        incidents = fetch_data('Incidents', 'incidents')
        transformed_incidents = transform_records(incidents, 'inc', 'IncidentNumber')
        
        # Fetch service requests
        servicereqs = fetch_data('servicereqs', 'service requests')
        transformed_servicereqs = transform_records(servicereqs, 'req', 'ServiceReqNumber')
        
        # Combine all records in a single list
        all_records = transformed_incidents + transformed_servicereqs
        
        if not all_records:
            print("No records found")
            return
        
        # Define fieldnames
        fieldnames = ['Owner', 'fecha_hoy', 'tipo', 'fecha_creacion', 'hora_creacion', 'idticket', 'asunto', 'estado']
        
        # Write combined data to a single CSV file
        csv_file = 'tickets_combinados.csv'
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_records)
        
        print(f"\n✓ Successfully exported {len(all_records)} records to {csv_file}")
        print(f"  - Incidents: {len(transformed_incidents)}")
        print(f"  - Service Requests: {len(transformed_servicereqs)}")
        
        # Write combined data to a single XLSX file
        xlsx_file = 'tickets_combinados.xlsx'
        wb = Workbook()
        ws = wb.active
        ws.title = "Tickets Combinados"
        
        ws.append(fieldnames)
        
        for record in all_records:
            row = [record.get(field, '') for field in fieldnames]
            ws.append(row)
        
        wb.save(xlsx_file)
        print(f"✓ Successfully exported {len(all_records)} records to {xlsx_file}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except Exception as e:
        print(f"Error processing data: {e}")

if __name__ == "__main__":
    fetch_incidents_and_servicereqs()