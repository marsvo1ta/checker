import os


def get_json_file_path(file_name):
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_script_directory, '..', 'json_data', 'calculate', f'{file_name}.json')

    return json_file_path

