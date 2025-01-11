import csv
from datetime import datetime

def parse_date(date_str):
    if not date_str:
        return ''
    try:
        return datetime.strptime(date_str.strip(), '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        print(f"Warning: Could not parse date '{date_str}'")
        return date_str

def parse_stations(input_file, output_file):
    data_rows = []
    columns = ['STA_NM_ANFR', 'ADM_ID', 'DEM_NM_COMSIS', 
              'DTE_IMPLANTATION', 'DTE_MODIF', 'DTE_EN_SERVICE']
    
    encodings = ['latin-1', 'iso-8859-1', 'cp1252', 'utf-8']
    
    for encoding in encodings:
        try:
            with open(input_file, 'r', encoding=encoding) as file:
                # Skip header
                header = file.readline()
                
                for line in file:
                    if not line.strip():
                        continue
                    
                    fields = line.strip().split(';')
                    
                    try:
                        row = {
                            'STA_NM_ANFR': fields[0],
                            'ADM_ID': fields[1],
                            'DEM_NM_COMSIS': fields[2],
                            'DTE_IMPLANTATION': parse_date(fields[3]),
                            'DTE_MODIF': parse_date(fields[4]),
                            'DTE_EN_SERVICE': parse_date(fields[5])
                        }
                        data_rows.append(row)
                    except (IndexError, ValueError) as e:
                        print(f"Error processing line: {line.strip()}")
                        continue
            
            break
        except UnicodeDecodeError:
            if encoding == encodings[-1]:
                raise Exception(f"Could not read file with any of the attempted encodings: {encodings}")
            continue

    # Save to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()
        writer.writerows(data_rows)

    print(f"Processed {len(data_rows)} rows and saved to {output_file}")

if __name__ == "__main__":
    input_file = 'data/SUP_STATION.txt'
    output_file = 'stations.csv'
    parse_stations(input_file, output_file)
