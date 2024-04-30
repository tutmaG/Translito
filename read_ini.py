import configparser

def load_config(file_path):
    ret_msg:dict={}
    config = configparser.ConfigParser()
    config.read(file_path)
    try:
        ret_msg["dbs"]=[config['databases']['main_db']]
        ret_msg["tables"]=[config["tables"]["first_table"],config["tables"]["second_table"]]
        ret_msg["msg"]="Success"

    except Exception as e:
        ret_msg["msg"]="ERROR"
        ret_msg["info"]=str(e)
        ret_msg["from"]="read_ini.py -> load_config()`s ERROR"
        ret_msg["dbs"]=[]
        ret_msg["tables"]=[]
    return ret_msg

if __name__ == "__main__":
    print(load_config("app.ini"))