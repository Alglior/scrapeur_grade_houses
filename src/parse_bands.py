import csv

def parse_frequency(freq_str):
    if not freq_str:
        return ''
    try:
        # Replace comma with dot for decimal numbers
        return str(float(freq_str.replace(',', '.')))
    except ValueError:
        print(f"Warning: Could not parse frequency '{freq_str}'")
        return freq_str

def parse_bands(input_file, output_file):
    data_rows = []
    columns = ['STA_NM_ANFR', 'BAN_ID', 'EMR_ID', 
              'BAN_NB_F_DEB', 'BAN_NB_F_FIN', 'BAN_FG_UNITE']
    
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
                            'BAN_ID': fields[1],
                            'EMR_ID': fields[2],
                            'BAN_NB_F_DEB': parse_frequency(fields[3]),
                            'BAN_NB_F_FIN': parse_frequency(fields[4]),
                            'BAN_FG_UNITE': fields[5]
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
    input_file = 'data/SUP_BANDE.txt'
    output_file = 'SUP_BANDE.csv'
    parse_bands(input_file, output_file)
