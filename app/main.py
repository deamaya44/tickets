import requests
import csv
import json
import time
import openpyxl
from openpyxl import Workbook
from datetime import datetime
from zoneinfo import ZoneInfo

def fetch_incidents_as_csv():
    """
    Fetch incidents from the API and save as CSV file
    """
    base_url = 'https://opengroup-amc-uat.ivanticloud.com/api/odata/businessobject/Incidents'
    headers = {
        'Authorization': 'rest_api_key=8EC080454B5047D8860F658F3CED9EF3',
        'rest_api_key': '8EC080454B5047D8860F658F3CED9EF3'
    }
    
    try:
        all_incidents = []
        skip = 0
        top = 100
        
        # Fetch all incidents with pagination
        while True:
            url = f'{base_url}?$top={top}&$skip={skip}'
            print(f"Fetching incidents {skip} to {skip + top}...")
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            incidents = data.get('value', [])
            
            if not incidents:
                print("No more incidents to fetch")
                break
            
            all_incidents.extend(incidents)
            print(f"Retrieved {len(incidents)} incidents. Total: {len(all_incidents)}")
            
            # Check if there are more incidents to fetch
            if len(incidents) < top:
                break
            
            skip += top
            time.sleep(1)  # Wait 1 second between requests
        
        if not all_incidents:
            print("No incidents found")
            return
        
        # Define only the fields we need (separated date and time)
        fieldnames = ['Owner', 'fecha_hoy', 'tipo', 'fecha_creacion', 'hora_creacion', 'idticket', 'asunto', 'estado']
        
        # Filter and transform incidents to include only needed fields
        filtered_incidents = []
        fecha_hoy = datetime.now(ZoneInfo("America/Bogota")).strftime('%Y-%m-%d %H:%M:%S')
        
        for incident in all_incidents:
            # Convert CreatedDateTime to Bogota timezone
            fecha_creacion_raw = incident.get('CreatedDateTime', '')
            fecha_creacion_formatted = ''
            hora_creacion_formatted = ''
            if fecha_creacion_raw:
                try:
                    # Parse ISO format datetime and convert to Bogota time
                    dt = datetime.fromisoformat(fecha_creacion_raw.replace('Z', '+00:00'))
                    dt_bogota = dt.astimezone(ZoneInfo("America/Bogota"))
                    fecha_creacion_formatted = dt_bogota.strftime('%Y-%m-%d')
                    hora_creacion_formatted = dt_bogota.strftime('%H:%M:%S')
                except:
                    fecha_creacion_formatted = fecha_creacion_raw
                    hora_creacion_formatted = ''
            
            filtered_incident = {
                'Owner': incident.get('Owner', ''),
                'fecha_hoy': fecha_hoy,
                'tipo': 'inc',  # Assuming all are incidents; adjust if you have logic to determine this
                'fecha_creacion': fecha_creacion_formatted,
                'hora_creacion': hora_creacion_formatted,
                'idticket': incident.get('IncidentNumber', ''),
                'asunto': incident.get('Subject', ''),
                'estado': incident.get('Status', '')
            }
            filtered_incidents.append(filtered_incident)
        
        # Write to CSV
        csv_file = 'incidents.csv'
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(filtered_incidents)
        
        print(f"Successfully exported {len(filtered_incidents)} incidents to {csv_file}")
        
        # Write to XLSX
        xlsx_file = 'incidents.xlsx'
        wb = Workbook()
        ws = wb.active
        ws.title = "Incidents"
        
        # Write headers
        ws.append(fieldnames)
        
        # Write data
        for incident in filtered_incidents:
            row = [incident.get(field, '') for field in fieldnames]
            ws.append(row)
        
        wb.save(xlsx_file)
        print(f"Successfully exported {len(filtered_incidents)} incidents to {xlsx_file}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except Exception as e:
        print(f"Error processing data: {e}")

if __name__ == "__main__":
    fetch_incidents_as_csv()