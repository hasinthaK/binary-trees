import os

__all__ = ['read_data_files']

def _read_values_from_file(file_path: str):
    '''
    Read values from data file provided & return a list.
    '''
    
    values = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Strip whitespace and newline characters
                value = line.strip()
                if value:  # Only add non-empty lines
                    values.append(value)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except IOError:
        print(f"Error reading file: {file_path}")
    
    return values

def read_data_files(file_type: str = 'insert' or 'search' or 'delete'):
    '''
    Read all the files for specified type & return as a dictionary in the 
    following format.
    - 1_1:[] -> denotes set1_data_1: [values] 
    - 1_2:[] -> denotes set1_data_2: [values] ...
    '''
    
    # read & perform ops from each file in order insert, search & delete
    insert_files_set_count = 2
    insert_files_data_count = 3
    
    file_values = {}
    
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # read all data files in order
    for set_count in range(1, insert_files_set_count + 1):
        for data_count in range(1, insert_files_data_count + 1):
            file_name = f'{file_type}_set{set_count}_data_{data_count}.txt'
            # Construct the full file path
            file_path = os.path.join(current_dir, file_name)
            
            # set dictionary with key & values as fileset:values
            file_values[f'{set_count}_{data_count}'] = _read_values_from_file(file_path)
    
    return file_values

