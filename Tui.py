from textual.app import App,on
from textual.widgets import Header,Footer,Static,Button,TextArea,Link
from textual.containers import ScrollableContainer
from textual.screen import ModalScreen
from pyfiglet import figlet_format

class AboutScreen(ModalScreen):
    BINDINGS = [('a','add_task','Add Task')]
    def compose(self):
        yield Static(figlet_format('TODOLIST','slant'))
        yield Static("Hey There This is My Project. So You Find some error please forgive me. 🙏")
        yield Link(text='Contribute On Github',url='https://github.com/shaneintentionboi06/To-do-list-textual')
    
    def action_add_task(self):
        Tid = self.app.DBcontrol.addtask('')
        Container = self.app.query_one('.Tasks',ScrollableContainer)
        Container.mount(Task(classes='Task',id=Tid))
        self.app.pop_screen()
    
class Task(Static):
    def compose(self):
        yield TextArea(id='TheTask')
        yield Button('Unmark',variant='success',id='Unmark')
        yield Button('Mark Done',variant='warning',id='Mark')
        # yield Button('Delete Task',variant='error',id='Delete')
        
    @on(Button.Pressed,'#Mark')
    def mark_done(self):
        mark = self.query_one('#Mark',Button)
        mark.add_class('Done')
        ID = self.id
        self.app.DBcontrol.mark(ID,1)
        # mark = self.query_one('#Mark',Button)
        # mark.set_class('UnMarked')
    @on(Button.Pressed,'#Unmark')
    def unmark_done(self):
        mark = self.query_one('#Mark',Button)
        mark.remove_class('Done')
        ID = self.id
        self.app.DBcontrol.mark(ID,0)
    @on(TextArea.Changed,'#TheTask')
    def updatedb(self):
        ID = self.id
        Text = self.query_one('#TheTask').text
        self.app.DBcontrol.updatetask(ID,Text)
    # @on(Button.Pressed,'#Delete')
    def on_mount(self, event):
        ID = self.id.lstrip('T')
        OldText = ''
        self.scroll_visible()
        self.focus()
        for task in self.app.existingtasks:
            if str(task[0]) == ID:
                OldText = task[1]
                if task[2] == 1:
                    self.mark_done()
        Text = self.query_one('#TheTask',TextArea)
        Text.load_text(OldText)
class TodoApp(App):
    BINDINGS = [('r','remove_task','Delete Task'),('a','add_task','Add Task'),('q','quit_app','Quit')]
    CSS_PATH = 'style.css'
    
    def __init__(self, driver_class = None, css_path = None, watch_css = False, ansi_color = False):
        self.existingtasks = self.app.DBcontrol.gettasks()
        # self.DBControl = DBcontrol
        super().__init__(driver_class, css_path, watch_css, ansi_color)
    
    def compose(self):
        yield Footer()
        yield ScrollableContainer(classes='Tasks')
        yield Header()
        # self.showextasks()
    def on_mount(self):
        self.showextasks()
    
    def showextasks(self):
        Container = self.query_one('.Tasks',ScrollableContainer)
        for task in self.existingtasks:
            Container.mount(Task(classes='Task',id="T"+str(task[0])))
        # self.app.notify("Restored Existing Tasks")
    
    def action_add_task(self):
        Tid = self.app.DBcontrol.addtask('')
        Container = self.query_one('.Tasks',ScrollableContainer)
        Container.mount(Task(classes='Task',id=Tid))
    
    def action_remove_task(self):
        theTask = self.query(Task)
        if theTask:
            ID = theTask.last().id
            theTask.last().remove()
            self.app.DBcontrol.remtask(ID)
        else:
            self.app.push_screen(AboutScreen(id='Aboutpage'))
            self.app.notify('No Task available to remove',severity='error')
    def action_quit_app(self):
        self.app.exit()
if __name__ == "__main__":
    from dbmanager import tododatabase
    DBcontrol = tododatabase()
    TodoApp().run()