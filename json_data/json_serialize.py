import json


def json_serialize(path: str):
    json_file_path = path

    with open(json_file_path, 'r') as json_file:
        json_content = json_file.read()

        try:
            json_data = json.loads(json_content)
        except json.JSONDecodeError as e:
            print(f'Error decoding JSON: {e}')
            return

    return json_data

