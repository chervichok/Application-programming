import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.view()

    def init_main(self):

        center_frame = Frame(root)
        center_frame.place(relx=.5, rely=.54, anchor="c", bordermode=OUTSIDE)

        self.tree = ttk.Treeview(center_frame, columns=('employee', 'salary', 'premium', 'tax'), height=15, show='headings')

        self.tree.column('employee', width=200, anchor=tk.CENTER)
        self.tree.column('salary', width=120, anchor=tk.CENTER)
        self.tree.column('premium', width=120, anchor=tk.CENTER)
        self.tree.column('tax', width=100, anchor=tk.CENTER)

        self.tree.heading('employee', text='Работник')
        self.tree.heading('salary', text='Зарплата')
        self.tree.heading('premium', text='Премия')
        self.tree.heading('tax', text='Налоги')

        self.tree.pack()

        btn_add = Button(root, text='Добавить', command=Child)
        btn_add.place(x=29, y=13)
        btn_search = Button(root, text='Поиск', command=Search)
        btn_search.place(x=110, y=13)

    def view(self):
        self.dictionary = {}
        [self.tree.insert('', 'end', values=[key, self.dictionary[key], (self.dictionary[key] * 0.20), (self.dictionary[key] + self.dictionary[key] * 0.20) * 0.05])
         for key in self.dictionary.keys()]


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить нового работника')
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        width = width // 2
        height = height // 2
        width = width - 200
        height = height - 115
        self.geometry('400x230+{}+{}'.format(width, height))
        self.resizable(False, False)

        label_employee = tk.Label(self, text='Фамилия и Имя', font=('Times new roman', 15))
        label_employee.place(x=50, y=50)
        label_salary = tk.Label(self, text='Зарплата',
                                font=('Times new roman', 15))
        label_salary.place(x=50, y=80)
        label_premium = tk.Label(self, text='Премия в %', font=('Times new roman', 15))
        label_premium.place(x=50, y=110)

        self.entry_employee = ttk.Entry(self)
        self.entry_employee.place(x=200, y=50)

        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=80)

        self.entry_premium = ttk.Entry(self)
        self.entry_premium.place(x=200, y=110)

        btn_add = Button(self, font=15, text='Добавить', command=self.update)
        btn_close = Button(self, font=15, text='Закрыть', command=self.destroy)

        btn_add.place(x=200, y=180)
        btn_close.place(x=300, y=180)

        self.grab_set()
        self.focus_set()

    def update(self):
        self.view.tree.insert('', 'end', values=[self.entry_employee.get(), int(self.entry_salary.get()), int(self.entry_salary.get()) * (int(self.entry_premium.get()) / 100), int(self.entry_salary.get()) * 0.06])
        new = {self.entry_employee.get(): int(self.entry_salary.get())}
        self.view.dictionary.update(new)
        self.destroy()


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск по фамилии')
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        width = width // 2
        height = height // 2
        width = width - 300
        height = height - 200
        self.geometry('600x400+{}+{}'.format(width, height))
        self.resizable(False, False)

        center_frame = Frame(self)
        center_frame.place(relx=.5, rely=.6, anchor="c", bordermode=OUTSIDE)

        self.tree1 = ttk.Treeview(center_frame, columns=('employee', 'salary', 'premium', 'tax'), height=13, show='headings')

        self.tree1.column('employee', width=200, anchor=tk.CENTER)
        self.tree1.column('salary', width=120, anchor=tk.CENTER)
        self.tree1.column('premium', width=120, anchor=tk.CENTER)
        self.tree1.column('tax', width=100, anchor=tk.CENTER)

        self.tree1.heading('employee', text='Работник')
        self.tree1.heading('salary', text='Зарплата')
        self.tree1.heading('premium', text='Премия')
        self.tree1.heading('tax', text='Налоги')

        self.tree1.pack()

        lbl = Label(self, text='Введите фамилию')
        lbl.place(x=130, y=13)
        lbl1 = Label(self, text='Введите премию')
        lbl1.place(x=130, y=48)

        self.entry_name = Entry(self)
        self.entry_name.place(x=260, y=15)
        self.entry_premium1 = Entry(self)
        self.entry_premium1.place(x=260, y=50)

        btn = Button(self, font=15, text='Поиск', command=self.result)
        btn.place(x=410, y=25)

        self.grab_set()
        self.focus_set()

    def result(self):

        try:
            [self.tree1.delete(i) for i in self.tree1.get_children()]
            self.tree1.insert('', 'end', values=[self.entry_name.get(), self.view.dictionary[self.entry_name.get()], int(self.view.dictionary[self.entry_name.get()] * (int(self.entry_premium1.get()) / 100)), (self.view.dictionary[self.entry_name.get()] * 0.06)])
        except KeyError:
            messagebox.showerror("Key Error", message='Такого работника нет')


if __name__ == "__main__":
    root = Tk()
    app = Main(root)
    app.place()
    root.title('Лабораторная работа №4.1')
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    width = width // 2
    height = height // 2
    width = width - 300
    height = height - 200
    root.geometry('600x400+{}+{}'.format(width, height))
    root.resizable(False, False)
    root.mainloop()
