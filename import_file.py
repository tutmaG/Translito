class File_import:
    def __init__(self, file_name):
        self.file_name = file_name

    def read_file(self):
        file_path="translated-words/"
        file=f'{file_path}{self.file_name}'
        raw_words=[]
        try:
            with open(file, 'r') as file:
                raw_words.append(file.read().split('\n'))
            raw_words = raw_words[0]
            del raw_words[-1]
            return raw_words
        except FileNotFoundError:
            return "Error: File not found"
        except Exception as e:
            return f"Error: {e}"
        
    def detecting_separator(self):
        ret_msg={}
        cont=0
        try:
            list = self.read_file()
            separator_test=list[1].split()[1]
            for i in range(len(list)):
                if  separator_test in list[i].split():
                    cont+=1
            if cont==len(list):
                ret_msg['msg']="Success"
                ret_msg['separator']=separator_test
            else:
                ret_msg['msg']="Faliure"
                ret_msg['separator']=""
            return ret_msg
        except Exception as e:
            ret_msg = {'msg': 'detecting_separator()`s ERROR',
                       'type':f'{e}',
                       'separator':'none'}
            return ret_msg
        
    def words_for_db(self):
        sorted_words={}
        try:
            separator=self.detecting_separator()['separator']
            if separator=="none":
                ret_msg={'msg':"faliure",
                    'words':[]}
                return ret_msg
            list=self.read_file()
            for i in list:
                parts = i.strip().split(separator)
                if len(parts) == 2:
                    key, value = parts[0].strip(),parts[1].strip()
                    sorted_words[key] = value
                else:
                    raise ValueError(f"Line '{i}' does not contain exactly one '{separator}'")
            ret_msg={'msg':"Success",
                    'words':sorted_words}
            return ret_msg
        except Exception as e:
            ret_msg = {'msg': 'words_for_db()`s ERROR',
                       'type':f'{e}',
                       'word':[]}
            return ret_msg

def main(file_name):
    val = File_import(file_name).words_for_db()
    return val






