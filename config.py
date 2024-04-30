import env_check
import json 
import time
from datetime import datetime 

def instalation():
    ret_msg: dict = {}
    try:
        dir_for_translated_words:dict =env_check.check_translated_word_dir()
        db:dict = env_check.check_db()
        os:dict = env_check.detect_os()
        translated_file:dict = env_check.check_translated_files()
        all_db_tables:dict={}
        if len(db['db_name'])==1:
            tables=env_check.check_table(db['db_name'][0])
            all_db_tables[db['db_name'][0]]=tables["table"]
        elif len(db['db_name'])>1:
            for db_ in db['db_name']:
                tables=env_check.check_table(db_)
                all_db_tables[db_]=tables['table']

        ret_msg['msg'] = "Success"
        ret_msg['update_time']=datetime.now().isoformat()
        ret_msg['db']=all_db_tables
        ret_msg['os']=os['OS']
        ret_msg['dir for translated words']=f'{dir_for_translated_words["translated_word_dir"][0]}/'
        ret_msg['translated files']=translated_file['files']
        return ret_msg
    except Exception as e:
        ret_msg = {'msg': 'instalation()`s ERROR',
                    'type':f'{e}'}
        return ret_msg
    
    
def config():
    ret_msg: dict={}
    try:
        data: dict = instalation()
        if not data['msg'] == "Success":
            ret_msg['msg']="ERROR"
            ret_msg['from']="instalation()"
        data.pop("msg")
        filename: str = "config.json"
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4) 
        ret_msg["msg"]='Success'
        ret_msg["info"]='Configuration successful'
    except Exception as e:
        ret_msg['msg']="ERROR"
        ret_msg['from']="instalation()"
        ret_msg["info"]=str(e)

    return ret_msg

if __name__=="__main__":
    print(config())