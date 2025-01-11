import csv

def parse_number(num_str):
    if not num_str:
        return ''
    try:
        # Replace comma with dot for decimal numbers
        return str(float(num_str.replace(',', '.')))
    except ValueError:
        # If it's not a number, return as is
        return num_str

def parse_antennas(input_file, output_file):
    data_rows = []
    columns = ['STA_NM_ANFR', 'AER_ID', 'TAE_ID', 'AER_NB_DIMENSION',
              'AER_FG_RAYON', 'AER_NB_AZIMUT', 'AER_NB_ALT_BAS', 'SUP_ID']
    
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
                            'AER_ID': fields[1],
                            'TAE_ID': fields[2],
                            'AER_NB_DIMENSION': parse_number(fields[3]),
                            'AER_FG_RAYON': fields[4],
                            'AER_NB_AZIMUT': parse_number(fields[5]),
                            'AER_NB_ALT_BAS': parse_number(fields[6]),
                            'SUP_ID': fields[7]
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
    input_file = 'data/SUP_ANTENNE.txt'
    output_file = 'SUP_ANTENNE.csv'
    parse_antennas(input_file, output_file)
