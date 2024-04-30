import json

def read_json_file(filename):
    ret_msg: dict = {}
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        ret_msg["msg"]="Success"
        ret_msg['data']=data
    except Exception as e:
        ret_msg["msg"]="ERROR"
        ret_msg['info']=e
        ret_msg['data']=[]
    return ret_msg

if __name__ == "__main__":
    filename = 'config.json'
    json_data = read_json_file(filename)
    if json_data:
        print(json_data)
