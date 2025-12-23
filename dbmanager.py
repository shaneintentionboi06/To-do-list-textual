import sqlite3
import os
class tododatabase:
    
    def __init__(self):
        self.DB,self.cursor = self.connect('Tododatabase.db')
    
    def connect(self,database):
        if os.path.exists(database):
            DB = sqlite3.connect(database)
            return DB,DB.cursor()
        else: 
            print("Making New Database")
            DB = sqlite3.connect(database)
            self.datasturcture(DB.cursor())
        return DB,DB.cursor()
                
    def datasturcture(self,Cursor):
        sturcturestring = '''
        create table todolist (
            ID Integer Primary Key autoincrement,
            Task text,
            Done integer not null default 0
        );
        '''
        Cursor.execute(sturcturestring)
        print('Database Sturctured')
        
    def addtask(self,task):
        self.cursor.execute('insert into todolist (Task) values (?)',(task,))
        self.DB.commit()
        self.cursor.execute('select ID from todolist')
        data = set()
        for row in self.cursor:
            data.add(row[0])
        return 'T'+str(max(data))
    def updatetask(self,id,task):
        self.cursor.execute('update todolist set Task = ?  where ID=?',(task,id.lstrip('T')) )
        self.DB.commit()
    def remtask(self,id):
        id = id.lstrip('T')
        self.cursor.execute('delete from todolist where ID= ?',(id,))
        self.DB.commit()
    def mark(self,id,Num):
        self.cursor.execute('update todolist set Done=? where ID= ? ',(Num,id.lstrip('T'),))
        self.DB.commit()
    def gettasks(self):
        self.cursor.execute("select ID, Task, Done from todolist")
        tasks = set()
        for task in self.cursor:
            tasks.add(task)
        return tasks
if __name__ == '__main__':
    # Dataobj = tododatabase()
    # print(Dataobj.addtask('Save the World'))
    # Dataobj.updatetask(1,'Hello World')
    # print('Done')
    # print(Dataobj.gettasks())
    # Dataobj.remtask("9")
    pass