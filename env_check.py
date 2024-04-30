import os 
import sys
from datetime import datetime, timedelta
import db_conn 

def date_diff(last_update_time,check_diff=None):
    ret_msg:dict={}
    last_update_time: datetime  = datetime.fromisoformat(last_update_time)
    current_time: datetime = datetime.now()
    time_difference: datetime = current_time - last_update_time
    ret_msg["time_difference"]=time_difference
    ret_msg["diff"]=""
    if check_diff:
        ret_msg["diff_val"]=check_diff
        if time_difference >= timedelta(days=check_diff):
            ret_msg["diff"]="True"
        else:
            ret_msg["diff"]="False"
    return ret_msg

            

def get_file_from_current_dir(search,current_directory=None):
    ret_msg: dict={}
    try:
        if current_directory==None:
            current_directory = os.getcwd()
        serching_files = [file for file in os.listdir(current_directory) if file.endswith(search)]
        if serching_files:
            ret_msg: dict={'msg':'Success',
                    'search':serching_files}
        else:
            ret_msg: dict={'msg':'faliure',
                    'search':[]}
        return ret_msg
    except Exception as e:
        ret_msg: dict={'msg':'get_file_from_current_dir()`s Error',
                       'info':e,
                       'search':[]}
        return ret_msg

def check_translated_word_dir():
    translated_word_dir: list = get_file_from_current_dir('translated-words')["search"]
    if translated_word_dir:
        ret_msg: dict={'msg':'Success',
                    'translated_word_dir':translated_word_dir}
    else:
         ret_msg: dict={'msg':'Not found',
                    'translated_word_dir':[]}
    return ret_msg


def check_db():
    db_files = get_file_from_current_dir('.db')["search"]
    if len(db_files)==0:
        ret_msg={'msg':'Not found',
                 'db_name':[]}
    else:
        ret_msg={'msg':'Success',
                 'db_name':db_files}
    return ret_msg

def check_table(db_name):
    ret_msg:dict={}
    try:
        tables=db_conn.DatabaseManager(db_name,"")
        tables_all=tables.show_tables()
        if tables_all['msg']=="Success":
            ret_msg["msg"]="Success"
            ret_msg["table"]=tables_all['tables']
        else:
            ret_msg["msg"]="faliure"
            ret_msg["table"]=[]
    except Exception as e:
        ret_msg["msg"]="check_translated_files()`s Error"
        ret_msg["info"]=str(e)
        ret_msg["table"]=[]
    return ret_msg
        

def check_config_json():
    config_file = get_file_from_current_dir('config.json')["search"]
    if len(config_file)==0:
        ret_msg={'msg':'False',
                 'config_file':[]}
    else:
        ret_msg={'msg':'Success',
                 'config_file':config_file}
    return ret_msg

def detect_os():
    ret_msg={"msg":"Success"}
    if sys.platform.startswith('win'):
        ret_msg["OS"]="Windows"
    elif sys.platform.startswith('linux'):
        ret_msg["OS"]="Linux"
    else:
        ret_msg={"msg":"ERROR"}
        ret_msg['OS']="Unknown"
    return ret_msg

def check_translated_files():
    ret_msg: dict={}
    try:
        dir=f'{check_translated_word_dir()["translated_word_dir"][0]}'
        files=get_file_from_current_dir(".txt",dir)["search"]
        ret_msg['msg']="Success"
        ret_msg['files']=files
        return ret_msg
    except Exception as e:
        ret_msg['msg']="check_translated_files()`s Error"
        ret_msg['info']=e
        ret_msg['files']=[]
    return ret_msg


if __name__ == "__main__":
    print(date_diff("2014-04-19T20:33:33.932559",3))