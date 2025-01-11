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

def parse_emissions(input_file, output_file):
    data_rows = []
    columns = ['EMR_ID', 'EMR_LB_SYSTEME', 'STA_NM_ANFR', 
              'AER_ID', 'EMR_DT_SERVICE']
    
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
                            'EMR_ID': fields[0],
                            'EMR_LB_SYSTEME': fields[1],
                            'STA_NM_ANFR': fields[2],
                            'AER_ID': fields[3],
                            'EMR_DT_SERVICE': parse_date(fields[4])
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
    input_file = 'data/SUP_EMETTEUR.txt'
    output_file = 'SUP_EMETTEUR.csv'
    parse_emissions(input_file, output_file)
