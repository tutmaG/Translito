import install
import env_check 
import config_json
import time
import read_ini
import db_conn
import sys
from rich import print 

def core():
    ret_msg: dict = {}
    try:
        json_file_check: dict = env_check.check_config_json()

        # checking if json file is exists
        if  not json_file_check['msg'] == "Success":
            print('[*]config file can`t find!', end='', flush=True)
            time.sleep(2)
            sys.stdout.write("\b" * 100) 
            try:
                print("\r[*]Automatic installation Starting...", end='', flush=True)
                install.main()
                time.sleep(2)
                sys.stdout.write("\b" * 100) 
            except Exception as e:
                ret_msg["msg"] = 'ERROR'
                ret_msg["from"] = 'core()`s ERROR --> $json file checking$'
                ret_msg["info"] = str(e)
                return ret_msg
            return core()
        
        try:
            json_file_name: str = json_file_check['config_file'][0]
            json_response: dict = config_json.read_json_file(json_file_name)
            json_data=json_response["data"]

            # cheking if table is exist . if not auto creating tables
            table_empty=False
            if len(json_data["db"])>0:
                table_check=json_data["db"]["Translation.db"]
                if len(table_check)==0:
                    table_empty:bool = True

            # cheking if db is exist . if not auto creating dbs
            if len(json_data['db'])==0 or table_empty:
                print("\r[*]Data base creating... ",end='', flush=True)
                time.sleep(2)
                sys.stdout.write("\b" * 100) 
                ini_file = read_ini.load_config("app.ini")
                if ini_file["msg"]=="ERROR":
                    print("[!!!]'app.ini' file can't found!!! --> $CRITICAL MESSAGE$")
                    print("[&]if you change it manually run 'python3 auto-fix.py --ini full'")
                    print("[!]Note:this feature is not avalible for version 0.0.1")
                    exit()
                #creating db and 2 tables
                first_table=db_conn.DatabaseManager(ini_file["dbs"][0],ini_file["tables"][0]).create_table_translation()
                second_table=db_conn.DatabaseManager(ini_file["dbs"][0],ini_file["tables"][1]).create_table_NOtranslation()
                install.main()
                return core()
            
            # auto_uptade
            last_update_time_str = json_data["update_time"]
            if last_update_time_str:
                time_difference= env_check.date_diff(last_update_time_str,3)
                if time_difference['diff']=="True":
                    print("[!]Auto update start...")
                    sys.stdout.write("\b" * 100) 
                    time.sleep(3)
                    install.main()
                    print("\r[*]Update is done!")
                    return core()
        except:
            print("\r[*]'config.json' is damaged, please dont touch it!\n[*]Try fix it...",end='', flush=True)
            sys.stdout.write("\b" * 100) 
            time.sleep(2)
            install.main()
            print("\r[*]'config.json' is fixed!")
            time.sleep(1)
            return core()

        if json_response['msg'] == 'Success':
            ret_msg["msg"] = 'Success'
            ret_msg["data"] = json_data
        else:
            ret_msg["msg"] = 'json file is Empty'
            ret_msg["data"] = []

    except Exception as e:
        ret_msg["msg"] = 'ERROR'
        ret_msg["from"] = "core()`s -->$CRITICAL ERROR$"
        ret_msg["info"] = str(e)
        ret_msg["data"] = []

    return ret_msg


if __name__ == "__main__":
   print(core())
