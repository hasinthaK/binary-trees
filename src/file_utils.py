import os
import csv

__all__ = [
    'read_data_files',
    'write_to_file',
    'compute_avg',
    'get_lines_to_write'
    ]

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

def read_data_files(op_type: str = 'insert' or 'search' or 'delete'):
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
            file_name = f'{op_type}_set{set_count}_data_{data_count}.txt'
            # Construct the full file path
            file_path = os.path.join(current_dir, file_name)
            
            # set dictionary with key & values as fileset:values
            file_values[f'{set_count}_{data_count}'] = _read_values_from_file(file_path)
    
    return file_values

def compute_avg(tree_type: str = 'bst' or 'rbt' or 'st', op_type: str = 'insert' or 'search' or 'delete'):
    '''
    Read the file denoted by the args & compute average for each line item, then append at the end.
    '''
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = f'{op_type}_{tree_type}_exec_times.csv'
    file_path = os.path.join(current_dir, file_name)
    
    # dict to group exec times
    exec_time_data = {}
    # dict to group height exec times
    height_exec_time_data = {}
    
    # Read the CSV file and compute averages
    with open(file_path, 'r', newline='\n') as file:
        reader = csv.reader(file)
        for row in reader:
            index, set_no, data_no, exec_time, height_exec_time, tree_type = row
            key = (set_no, data_no, tree_type)
            
            # create exec time data dict grouped by key
            if key not in exec_time_data:
                exec_time_data[key] = []
            exec_time_data[key].append(float(exec_time))
            
            # create height exec time data dict grouped by key
            if key not in height_exec_time_data:
                height_exec_time_data[key] = []
            height_exec_time_data[key].append(float(height_exec_time))
    
    # Compute averages
    averages = {key: sum(values) / len(values) for key, values in exec_time_data.items()}
    
    # compute height exec time averages
    height_averages = {key: sum(values) / len(values) for key, values in height_exec_time_data.items()}
    
    # Write the updated data back to the CSV file
    temp_file_path = os.path.join(current_dir, f'temp_{file_name}')
    with open(file_path, 'r', newline='\n') as input_file, open(temp_file_path, 'w', newline='\n') as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)
        for row in reader:
            index, set_no, data_no, exec_time, height_exec_time, tree_type = row
            key = (set_no, data_no, tree_type)
            avg_exec_time = averages[key]
            avg_height_exec_time = height_averages[key]
            writer.writerow(row + [f'{avg_exec_time:.6f}'] + [f'{avg_height_exec_time:.6f}'])
    
    print(f'Averaged for {file_name}')
    # Replace the original file with the updated one
    os.replace(temp_file_path, file_path)

def _construct_line_to_write(index: int, set_no: int, data_no: int, exec_time: float, height_exec_time: float, tree_type: str = 'bst' or 'rbt' or 'st'):
    '''
    Create a line item to be written into the CSV file. This function 
    denotes the strcuture of the csv files written.
    '''
    return f'{index},{set_no},{data_no},{exec_time},{height_exec_time},{tree_type}'

def write_to_file(line: str, tree_type: str = 'bst' or 'rbt' or 'st', op_type: str = 'insert' or 'search' or 'delete'):
    '''
    Write the provided line to file specified.
    '''
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = f'{op_type}_{tree_type}_exec_times.csv'
    file_path = os.path.join(current_dir, file_name)
    
    print(f'Writing to file: {file_name}')
    
    with open(file_path, 'a', newline='\n') as file:
        file.write(line + '\n')

def get_lines_to_write(index: int, exec_times: tuple, tree_type: str = 'bst' or 'rbt' or 'st'):
    ([one_1, one_2, one_3, two_1, two_2, two_3], [h_one_1, h_one_2, h_one_3, h_two_1, h_two_2, h_two_3]) = exec_times
    lines = []
    
    lines.append(_construct_line_to_write(index, 1, 1, one_1.total_seconds(), h_one_1.total_seconds(), tree_type))
    lines.append(_construct_line_to_write(index, 1, 2, one_2.total_seconds(), h_one_2.total_seconds(), tree_type))
    lines.append(_construct_line_to_write(index, 1, 3, one_3.total_seconds(), h_one_3.total_seconds(), tree_type))
    lines.append(_construct_line_to_write(index, 2, 1, two_1.total_seconds(), h_two_1.total_seconds(), tree_type))
    lines.append(_construct_line_to_write(index, 2, 2, two_2.total_seconds(), h_two_2.total_seconds(), tree_type))
    lines.append(_construct_line_to_write(index, 2, 3, two_3.total_seconds(), h_two_3.total_seconds(), tree_type))
    
    return lines