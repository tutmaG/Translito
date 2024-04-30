import db_conn 
from rich import print

class Commands:
    def __init__(self,db_name=None) -> None:
        self.db_name=db_name
        self.ret_msg=None

    def help():
        print("\nThis is small CLI app which is translator and can use as store of words , english to georgia and reverse")
        print("To see avalibel commands run 'avalible commands' or 'AC'\n")

    def avalible_commands():
        avalible_commands: dict={'Commands':['help(H)','exit(E)','avalible_commands(AC)','show word(SW)'],
                                 'Modes':["write(W)"] 
                                 }
        return avalible_commands
    
    def show_write_db(self,table_name):
        show_all=db_conn.DatabaseManager(self.db_name,table_name).show_all()
        if show_all['msg']=="ERROR":
            self.ret_msg="ERROR"
        if show_all["msg"]=='Success':
            self.ret_msg=show_all['rows']
        return self.ret_msg

    def show_translated_db():
        pass

class Mode:
    def __init__(self,db_name=None) -> None:
        self.db_name = db_name
        self.ret_msg:dict = {}

    def write(self,table_name,en_word,flag=None):
        help_menu="This is writing mode. you can just tipe word and prass enter and this word add automaticl is stored.\nUse 'back' or 'B' for return Command Interface. "
        if flag=="help" or flag=="H":
           self.ret_msg=help_menu
        else:
            write_conn=db_conn.DatabaseManager(self.db_name,table_name)
            word=write_conn.add_item_writed_db(en_word)
            if word["msg"]=="ERROR":
                self.ret_msg="ERROR"
            if word['msg']=="Entry already exists":
                self.ret_msg=word["msg"]
            if word['msg']=="New row added":
                self.ret_msg=word["value"]
        return self.ret_msg

if __name__=="__main__":
    msg=Mode("Translation.db").write("only_en","zoia1")
    print(msg)

