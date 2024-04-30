import sqlite3

class DatabaseManager:
    def __init__(self, db_name ,table_name):
        self.db_name = db_name
        self.table_name = table_name
        self.ret_msg:dict = {}

#--------------done----------------
    def execute_query(self, query, *args):
        ret_msg:dict={}
        try:
            conn = sqlite3.connect(self.db_name) 
            cursor = conn.cursor()
            cursor.execute(query, args)
            conn.commit()
            data = cursor.fetchall()
            ret_msg["msg"]="Sucess"
            ret_msg['data']=data
        except Exception as e:
            ret_msg["msg"]="ERROR"
            ret_msg['data']=[]
            ret_msg['from']="execute_query()"
            ret_msg["info"]=str(e)
        return ret_msg
#==============================================================
#====================DONE======================================
    def create_table_translation(self):
        ret_msg:dict = {}
        try:
            check_table = self.show_tables()['tables']
            if self.table_name in check_table:
                ret_msg['msg']="Table already exists"
                ret_msg['table_name']=self.table_name
            else:
                query = f'''CREATE TABLE IF NOT EXISTS {self.table_name} (
                                id INTEGER PRIMARY KEY,
                                en_words TEXT NOT NULL,
                                ge_words TEXT NOT NULL
                            )'''
                query_check_=self.execute_query(query)
                if  query_check_["msg"]=="ERROR":
                    ret_msg['msg']="ERROR"
                    ret_msg['from']=f"{query_check_['from']} --> create_table_translation()"
                    ret_msg['info']=query_check_["info"]
                    ret_msg['table_name']=None
                else:
                    ret_msg['msg']="Success"
                    ret_msg['info']="New table created"
                    ret_msg['table_name']=self.table_name
        except Exception as e:
                ret_msg['msg']="ERROR"
                ret_msg['from']="create_table_translation()"
                ret_msg['info']=str(e)
        return ret_msg
#==============================================================

    def create_table_NOtranslation(self):
        try:
            check_db = self.show_tables()['tables']
            if self.table_name in check_db:
                ret_msg = {'msg': "Table already exists",
                        'table_name': self.table_name}
                return ret_msg
            else:
                query = f'''CREATE TABLE IF NOT EXISTS {self.table_name} (
                                id INTEGER PRIMARY KEY,
                                NO_translated_words TEXT NOT NULL
                            )'''
                self.execute_query(query)
                ret_msg = {'msg': "New table created",
                            "table_name": self.table_name}
                return ret_msg
        except Exception as e:
            ret_msg = {'msg': 'create_table_NOtranslation()`s ERROR',
                       'type':f'{e}'}
            return ret_msg

    def show_tables(self):
        ret_msg:dict=[]
        try:
            query = "SELECT name FROM sqlite_master WHERE type='table';"
            tables:list = self.execute_query(query)["data"]
            all_tables = [table[0] for table in tables]
            if len(all_tables)==0:
                ret_msg = {'msg': 'No tables found',
                           'tables': []}
            else:
                ret_msg = {'msg': 'Success',
                           'tables': all_tables}
            return ret_msg
        except Exception as e:
            ret_msg = {'msg': 'show_tables()`s ERROR',
                       'type':f'{e}'}
            return ret_msg

    def show_columns(self):
        try:
            query = f"PRAGMA table_info({self.table_name})"
            columns_info = self.execute_query(query)
            column_names = [column[1] for column in columns_info]
            if len(column_names) == 0:
                ret_msg = {'msg': 'No table found',
                           'column_names':[]}
            else:
                ret_msg = {'msg': 'Success',
                           'column_names': column_names}
            return ret_msg
        except Exception as e:
            ret_msg = {'msg': 'show_columns()`s ERROR',
                       'type':str(e)}
            return ret_msg

    def add_item_translated_db(self,en_word,ge_word):
        try:
            chechk_item =  self.show_one_item_en(en_word)
            if len(chechk_item)==0:
                query = f"INSERT OR IGNORE INTO {self.table_name} (en_words, ge_words) VALUES (?, ?)"
                self.execute_query(query, en_word, ge_word)
                ret_msg = {'msg': 'New row added',
                            'value': f" '{en_word}' <---> {ge_word}' "}
            else:
                ret_msg = {'msg': 'Entry already exists',
                            'value':''}
            return ret_msg
        except Exception as e:
            ret_msg = {'msg': 'add_item()`s ERROR',
                       'type':f'e'}
            return ret_msg
#====================DONE======================================     
    def show_all(self):
        all_rows:list = []
        try:
            query = f"SELECT * FROM {self.table_name}"
            query_check = self.execute_query(query)
            if query_check["msg"]=="ERROR":
                self.ret_msg["msg"]="ERROR"
                self.ret_msg["rows"]=[]
                self.ret_msg["from"]=f'{query_check["from"]} --> show_all()'
                self.ret_msg["info"]=query_check['info']
            else:
                rows=query_check['data']
                for row in rows:
                    all_rows.append(row)
                self.ret_msg["msg"]="Success"
                self.ret_msg["rows"]=all_rows
        except Exception as e:
            self.ret_msg["msg"]="ERROR"
            self.ret_msg["rows"]=[]
            self.ret_msg["from"]="show_all()"
            self.ret_msg["info"]=str(e)
        return self.ret_msg
#==============================================================
#====================DONE======================================
    def add_item_writed_db(self,en_word:str):
        ret_msg:dict={}
        try:
            chechk_item =  self.show_one_item_NO_translated_words(en_word)
            if chechk_item["msg"]=="ERROR":
                ret_msg['msg']="ERROR"
                ret_msg['from']=f'{chechk_item["from"]} --> add_item_writed_db()'
                ret_msg["value"]=None
            else:
                if len(chechk_item["item"])==0:
                    query = f"INSERT OR IGNORE INTO {self.table_name} (NO_translated_words) VALUES (?)"
                    check_=self.execute_query(query, en_word)
                    ret_msg['msg'] = 'New row added'
                    ret_msg['value'] = en_word
                else:
                    ret_msg['msg'] = 'Entry already exists'
                    ret_msg['value'] = None
                
        except Exception as e:
            ret_msg["msg"]="ERROR"
            ret_msg["from"]="add_item_writed_db()"
            ret_msg['info']=str(e)
        return ret_msg
#==============================================================
#====================DONE======================================
    def show_one_item_NO_translated_words(self,en_word):
        ret_msg:dict={}
        try:
            query = f"SELECT * FROM {self.table_name} WHERE NO_translated_words = ?"
            item = self.execute_query(query,en_word)
            if item["msg"]=="ERROR":
                ret_msg['msg']="ERROR"
                ret_msg['from']=f'{item["from"]} ---> show_one_item_NO_translated_words()'
                ret_msg['info']=item["info"]
                ret_msg["item"]=""
            else:
                if len(item)==0:
                    ret_msg['msg']="Not found"
                    ret_msg["item"]=item["data"]
                else:
                    ret_msg['msg']="Success"
                    ret_msg["item"]=item["data"]
        except Exception as e:
            ret_msg['msg']="ERROR"
            ret_msg["item"]=""
            ret_msg['from']="show_one_item_NO_translated_words()"
            ret_msg['info']=str(e)
        return ret_msg
#==============================================================

    def show_one_item_en(self,en_word):
        try:
           query = f"SELECT * FROM {self.table_name} WHERE en_words = ?"
           item = self.execute_query(query,en_word)
           if item["msg"]=="ERROR":
                self.ret_msg["msg"] ="ERROR"
                self.ret_msg["from"]=f"{item["from"]} ---> show_one_item_en()"
                self.ret_msg['info']=item['info']
                self.ret_msg['item']=None
           else:
               self.ret_msg=item['data']
           return self.ret_msg
        except Exception as e:
            self.ret_msg["msg"] ="ERROR"
            self.ret_msg["from"]="show_one_item_en()"
            self.ret_msg['info']=str(e)
            return self.ret_msg
        
if __name__=="__main__":
    maxo=DatabaseManager("Translation.db","only_en").show_all()
    # maxo=DatabaseManager("Translation.db","").show_tables()
    print(maxo)