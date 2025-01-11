import csv

def parse_coordinates(input_file, output_file):
    data_rows = []
    
    # Define column names based on the format
    columns = ['SUP_ID', 'STA_NM_ANFR', 'NAT_ID', 'Latitude', 'Longitude', 
              'SUP_NM_HAUT', 'TPO_ID', 'ADR_LB_LIEU', 'ADR_LB_ADD1', 
              'ADR_LB_ADD2', 'ADR_LB_ADD3', 'ADR_NM_CP', 'COM_CD_INSEE']
    
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
                        # Extract coordinates
                        lat_deg = int(fields[3])
                        lat_min = int(fields[4])
                        lat_sec = int(fields[5])
                        lat_dir = fields[6]
                        lon_deg = int(fields[7])
                        lon_min = int(fields[8])
                        lon_sec = int(fields[9])
                        lon_dir = fields[10]

                        # Convert to decimal degrees
                        latitude = lat_deg + lat_min / 60 + lat_sec / 3600
                        if lat_dir == 'S':
                            latitude = -latitude

                        longitude = lon_deg + lon_min / 60 + lon_sec / 3600
                        if lon_dir == 'W':
                            longitude = -longitude

                        # Create row with all data
                        row = {
                            'SUP_ID': fields[0],
                            'STA_NM_ANFR': fields[1],
                            'NAT_ID': fields[2],
                            'Latitude': f"{latitude:.6f}",
                            'Longitude': f"{longitude:.6f}",
                            'SUP_NM_HAUT': fields[11],
                            'TPO_ID': fields[12],
                            'ADR_LB_LIEU': fields[13],
                            'ADR_LB_ADD1': fields[14],
                            'ADR_LB_ADD2': fields[15],
                            'ADR_LB_ADD3': fields[16],
                            'ADR_NM_CP': fields[17],
                            'COM_CD_INSEE': fields[18] if len(fields) > 18 else ''
                        }
                        
                        data_rows.append(row)
                    except (ValueError, IndexError) as e:
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
    input_file = 'data/SUP_SUPPORT.txt'
    output_file = 'antenna_data.csv'
    parse_coordinates(input_file, output_file)
