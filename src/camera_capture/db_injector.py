import json


def store_data(data):
    with open("data.json", "a") as file:
        json_data = json.dumps(data)
        file.write(json_data)
    print(f"Storing data: {json_data}")
