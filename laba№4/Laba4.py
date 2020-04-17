import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Combobox
import sqlite3
from datetime import *
import datetime


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):

        header_frame = Frame(root, bg="#CD853F", width=2000, height=50, borderwidth=10)
        header_frame.place(rely=.15, anchor="c", bordermode=OUTSIDE)

        center_frame = Frame(root)
        center_frame.place(relx=.5, rely=.54, anchor="c", bordermode=OUTSIDE)

        self.tree = ttk.Treeview(center_frame, columns=('ID', 'date', 'client', 'service', 'cost'), height=25, show='headings')

        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('date', width=200, anchor=tk.CENTER)
        self.tree.column('client', width=280, anchor=tk.CENTER)
        self.tree.column('service', width=250, anchor=tk.CENTER)
        self.tree.column('cost', width=200, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('date', text='Дата')
        self.tree.heading('client', text='Фамилия и Имя')
        self.tree.heading('service', text='Услуга')
        self.tree.heading('cost', text='Цена')

        self.tree.pack()

        self.delete_img = tk.PhotoImage(file='delete.gif')
        self.change_img = tk.PhotoImage(file='pencil.gif')
        self.add_img = tk.PhotoImage(file='add.gif')
        self.refresh_img = tk.PhotoImage(file='refresh.gif')
        self.search_img = tk.PhotoImage(file='search.gif')
        self.exit_img = tk.PhotoImage(file='exit.gif')

        btn_new_client = Button(root, text='Добавить клиента', bg='#FFE4C4', bd=0, image=self.add_img, compound=TOP, fg='black', font=('Times new roman', 15), command=Child)
        btn_search_main = Button(root, text='Поиск', bg='#FFE4C4', bd=0, image=self.search_img, compound=TOP, fg='black', font=('Times new roman', 15), command=Child1)
        btn_refresh = Button(root, text='Обновить', bg='#FFE4C4', bd=0, image=self.refresh_img, compound=TOP, fg='black', font=('Times new roman', 15), command=self.refresh)
        btn_change = Button(root, text='Редактировать', bg='#FFE4C4', bd=0, image=self.change_img, compound=TOP, fg='black', font=('Times new roman', 15), command=Child2)
        btn_info = Button(root, text='Обновления за последнии сутки', width=28, bg='#FFE4C4', fg='black', font=('Times new roman', 15), command=self.info)
        btn_remove = Button(root, text='Удаление', bg='#FFE4C4', bd=0, image=self.delete_img, compound=TOP, fg='black', font=('Times new roman', 15), command=Child3)
        btn_exit = Button(root, bg='#FFE4C4', width=100, height=100, bd=0, image=self.exit_img, compound=TOP, fg='black', command=self.exit)

        btn_new_client.place(x=20, y=10)
        btn_refresh.place(x=800, y=10)
        btn_search_main.place(x=910, y=10)
        btn_change.place(x=200, y=10)
        btn_info.place(x=350, y=101)
        btn_remove.place(x=350, y=10)
        btn_exit.place(x=890, y=700)

    def records(self, date, client, service, cost):
        self.db.insert_data(date, client, service, cost)
        self.view_records()

    def update_records(self, date, client, service, cost):
        self.db.c.execute('UPDATE barbershop SET date=?, client=?, service=?, cost=? WHERE id=?', (date, client, service, cost, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def remove(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM barbershop WHERE id = ?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def refresh(self):
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM barbershop''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]

    def info(self):
        date_today = datetime.date.today()
        date_yesterday = date_today - timedelta(days=1)
        today = date_today.strftime("%d.%m.%Y")
        yesterday = date_yesterday.strftime("%d.%m.%Y")
        self.db.c.execute('''SELECT * FROM barbershop  WHERE date = ? OR date = ? ORDER BY date ASC''', (today, yesterday,))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]

    def exit(self):
        root.destroy()
        self.db.conn.close()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):

        self.title('Добавить нового клиента')
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        width = width // 2
        height = height // 2
        width = width - 200
        height = height - 130
        self.geometry('400x260+{}+{}'.format(width, height))
        self.config(bg="#FFE4C4")
        self.resizable(False, False)

        label_date = tk.Label(self, bg='#FFE4C4', text='Дата посещения', font=('Times new roman', 15))
        label_date.place(x=50, y=50)
        label_client = tk.Label(self, bg='#FFE4C4', text='Фамилия и Имя', font=('Times new roman', 15))
        label_client.place(x=50, y=80)
        label_select = tk.Label(self, bg='#FFE4C4', text='Услуга', font=('Times new roman', 15))
        label_select.place(x=50, y=110)
        label_sum = tk.Label(self, bg='#FFE4C4', text='Цена', font=('Times new roman', 15))
        label_sum.place(x=50, y=140)

        self.entry_date = ttk.Entry(self)
        self.entry_date.place(x=200, y=50)

        self.entry_client = ttk.Entry(self)
        self.entry_client.place(x=200, y=80)

        self.entry_service = ttk.Entry(self)
        self.entry_service.place(x=200, y=110)

        self.entry_cost = ttk.Entry(self)
        self.entry_cost.place(x=200, y=140)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=200)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=200)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_date.get(), self.entry_client.get(), self.entry_service.get(), self.entry_cost.get()))

        self.grab_set()
        self.focus_set()


class Child1(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child1()
        self.view = app
        self.db = db

    def init_child1(self):

        self.title('Поиск')
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        width = width // 2
        height = height // 2
        width = width - 200
        height = height - 100
        self.geometry('400x200+{}+{}'.format(width, height))
        self.config(bg="#FFE4C4")
        self.resizable(False, False)

        lbl_search = Label(self, font=('Times new roman', 20), bg="#FFE4C4", text='Выберите параметр поиска')

        lbl_search.place(x=40, y=20)

        self.combobox = Combobox(self, font=('Times new roman', 18), values=[u'ID', u'Дата', u'Имя фамилия', u'Услуга', u'Цена'])
        self.combobox.current(0)
        self.combobox.place(x=72, y=80)

        btn_accept = Button(self, font=('Times new roman', 18), text='Выбрать', command=self.result)
        btn_exit = Button(self, font=('Times new roman', 18), text='Отмена', command=self.destroy)

        btn_accept.place(x=180, y=140)
        btn_exit.place(x=300, y=140)

    def result(self):
        if self.combobox.get() == 'ID':
            ID()
        elif self.combobox.get() == 'Дата':
            Date()
        elif self.combobox.get() == 'Имя фамилия':
            Client()
        elif self.combobox.get() == 'Услуга':
            Service()
        elif self.combobox.get() == 'Цена':
            Cost()

        self.destroy()


class Child2(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app

    def init_edit(self):

        self.title('Редактировать клиента')
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        width = width // 2
        height = height // 2
        width = width - 200
        height = height - 130
        self.geometry('400x260+{}+{}'.format(width, height))
        self.config(bg="#FFE4C4")
        self.resizable(False, False)

        self.btn_edit = ttk.Button(self, text='Редактировать')
        self.btn_edit.place(x=200, y=200)
        self.btn_edit.bind('<Button-1>', lambda event: self.view.update_records(self.entry_date.get(), self.entry_client.get(), self.entry_service.get(), self.entry_cost.get()))

        self.btn_ok.destroy()

        self.grab_set()
        self.focus_set()


class Child3(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child3()
        self.view = app

    def init_child3(self):

        self.title('Подтверждение')
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        width = width // 2
        height = height // 2
        width = width - 150
        height = height - 100
        self.geometry('300x200+{}+{}'.format(width, height))
        self.config(bg="#FFE4C4")
        self.resizable(False, False)

        lbl_info = Label(self, font=('Times new roman', 23), bg="#FFE4C4", text='Вы уверены?')
        lbl_info.place(x=60, y=50)

        btn_yes = Button(self, width=7, font=('Times new roman', 20), text='Да', command=self.yes)
        btn_no = Button(self, width=7, font=('Times new roman', 20), text='Нет', command=self.no)

        btn_yes.place(x=20, y=110)
        btn_no.place(x=170, y=110)

        self.grab_set()
        self.focus_set()

    def yes(self):
        self.view.remove()
        self.destroy()

    def no(self):
        self.destroy()


class ID(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_ID()
        self.view = app
        self.db = db

    def init_ID(self):
        self.title('Поиск по ID')
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        width = width // 2
        height = height // 2
        width = width - 300
        height = height - 50
        self.geometry('600x100+{}+{}'.format(width, height))
        self.config(bg="#FFE4C4")
        self.resizable(False, False)

        lbl = Label(self, font=('Times new roman', 20), text='Введите ID', bg="#FFE4C4")
        lbl.place(x=20, y=30)

        self.entr = Entry(self, width=15, font=('Times new roman', 20))
        self.entr.place(x=170, y=30)

        btn = Button(self, font=('Times new roman', 17), text='Поиск', command=self.if_id)
        btn_closed = Button(self, font=('Times new roman', 17), text='Закрыть', command=self.closed)
        btn.place(x=393, y=25)
        btn_closed.place(x=480, y=25)

    def if_id(self):
        self.db.c.execute('''SELECT id, date, client, service, cost FROM barbershop WHERE id = ?''', (self.entr.get(),))
        [self.view.tree.delete(i) for i in self.view.tree.get_children()]
        [self.view.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]

    def closed(self):
        self.destroy()
        self.view.view_records()


class Date(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_date()
        self.view = app
        self.db = db

    def init_date(self):
        self.title('Поиск по дате')
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        width = width // 2
        height = height // 2
        width = width - 300
        height = height - 50
        self.geometry('600x100+{}+{}'.format(width, height))
        self.config(bg="#FFE4C4")
        self.resizable(False, False)

        lbl = Label(self, font=('Times new roman', 19), text='Введите дату', bg="#FFE4C4")
        lbl.place(x=20, y=30)

        self.entr = Entry(self, width=15, font=('Times new roman', 20))
        self.entr.place(x=170, y=30)

        btn = Button(self, font=('Times new roman', 17), text='Поиск', command=self.if_date)
        btn_closed = Button(self, font=('Times new roman', 17), text='Закрыть', command=self.closed)
        btn.place(x=393, y=25)
        btn_closed.place(x=480, y=25)

    def if_date(self):
        self.db.c.execute('''SELECT id, date, client, service, cost FROM barbershop WHERE date = ?''', (self.entr.get(),))
        [self.view.tree.delete(i) for i in self.view.tree.get_children()]
        [self.view.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]

    def closed(self):
        self.destroy()
        self.view.view_records()


class Client(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_client()
        self.view = app
        self.db = db

    def init_client(self):
        self.title('Поиск по клиенту')
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        width = width // 2
        height = height // 2
        width = width - 300
        height = height - 50
        self.geometry('600x100+{}+{}'.format(width, height))
        self.config(bg="#FFE4C4")
        self.resizable(False, False)

        lbl = Label(self, font=('Times new roman', 15), bg="#FFE4C4", text='Введите фамилию и имя')
        lbl.place(x=20, y=30)

        self.entr = Entry(self, width=15, font=('Times new roman', 15))
        self.entr.place(x=240, y=30)

        btn = Button(self, font=('Times new roman', 15), text='Поиск', command=self.if_date)
        btn_closed = Button(self, font=('Times new roman', 15), text='Закрыть', command=self.closed)
        btn.place(x=410, y=25)
        btn_closed.place(x=490, y=25)

    def if_date(self):
        self.db.c.execute('''SELECT id, date, client, service, cost FROM barbershop WHERE client = ?''', (self.entr.get(),))
        [self.view.tree.delete(i) for i in self.view.tree.get_children()]
        [self.view.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]

    def closed(self):
        self.destroy()
        self.view.view_records()


class Service(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_service()
        self.view = app
        self.db = db

    def init_service(self):
        self.title('Поиск по услуге')
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        width = width // 2
        height = height // 2
        width = width - 300
        height = height - 50
        self.geometry('600x100+{}+{}'.format(width, height))
        self.config(bg="#FFE4C4")
        self.resizable(False, False)

        lbl = Label(self, font=('Times new roman', 17), text='Введите услугу', bg="#FFE4C4")
        lbl.place(x=17, y=30)

        self.entr = Entry(self, width=15, font=('Times new roman', 19))
        self.entr.place(x=178, y=30)

        btn = Button(self, font=('Times new roman', 17), text='Поиск', command=self.if_id)
        btn_closed = Button(self, font=('Times new roman', 17), text='Закрыть', command=self.closed)
        btn.place(x=393, y=25)
        btn_closed.place(x=480, y=25)

    def if_id(self):
        self.db.c.execute('''SELECT id, date, client, service, cost FROM barbershop WHERE service = ?''', (self.entr.get(),))
        [self.view.tree.delete(i) for i in self.view.tree.get_children()]
        [self.view.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]

    def closed(self):
        self.destroy()
        self.view.view_records()


class Cost(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_cost()
        self.view = app
        self.db = db

    def init_cost(self):
        self.title('Поиск по цене')
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        width = width // 2
        height = height // 2
        width = width - 300
        height = height - 50
        self.geometry('600x100+{}+{}'.format(width, height))
        self.config(bg="#FFE4C4")
        self.resizable(False, False)

        lbl = Label(self, font=('Times new roman', 19), text='Введите цену', bg="#FFE4C4")
        lbl.place(x=20, y=30)

        self.entr = Entry(self, width=15, font=('Times new roman', 20))
        self.entr.place(x=170, y=30)

        btn = Button(self, font=('Times new roman', 17), text='Поиск', command=self.if_id)
        btn_closed = Button(self, font=('Times new roman', 17), text='Закрыть', command=self.closed)
        btn.place(x=393, y=25)
        btn_closed.place(x=480, y=25)

    def if_id(self):
        self.db.c.execute('''SELECT id, date, client, service, cost FROM barbershop WHERE cost = ?''', (self.entr.get(),))
        [self.view.tree.delete(i) for i in self.view.tree.get_children()]
        [self.view.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]

    def closed(self):
        self.destroy()
        self.view.view_records()


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('barbershop.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS barbershop (id integer primary key, date date, client text, service text, cost integer)''')
        self.conn.commit()

    def insert_data(self, date, client, service, cost):
        self.c.execute('''INSERT INTO barbershop(date, client, service, cost) VALUES (?, ?, ?, ?)''', (date, client, service, cost))
        self.conn.commit()


if __name__ == "__main__":
    root = Tk()
    db = DB()
    app = Main(root)
    app.place()
    root.title('Лабораторная работа №4')
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    width = width // 2
    height = height // 2
    width = width - 500
    height = height - 400
    root.geometry('1000x800+{}+{}'.format(width, height))
    root.config(bg="#FFE4C4")
    root.resizable(False, False)
    root.mainloop()
