import requests
import json
import tkinter as tk  # tkinter - graphical user interface library
from tkinter.ttk import Combobox
from PIL import Image as Pilimage  # для изменения размера изображения установить Pillow в pip
from PIL import ImageTk  # преобразовывает изображение из PIL для tkinter
# from tkinter.scrolledtext import ScrolledText
# from tkinter import messagebox as mb
from Labels import Labels
from DraWidgets import DraWidgets
from ShowVacancies import ShowVacancies
from CountryRegionCity import CountryRegionCity
from Keywords_QtyVacancies import Keywords_QtyVacancies


class HeadHunter(Labels, DraWidgets, CountryRegionCity, ShowVacancies, Keywords_QtyVacancies):
    """create and run mane window"""

    def __init__(self, width=590, height=450, title="Поиск Вакансий HeadHanter.ru", icon="resourses/hh.ico"):
        url = "https://api.hh.ru/areas"  # список всех городов, регионов, стран
        req = requests.get(url)
        data = req.content.decode()
        req.close()
        self.areas = json.loads(data)  # список всех городов грузим из файла json

        self.win = tk.Tk()  # создание основного окна
        self.win.geometry(f"{width}x{height}+250+150")  # size and padding of the window on screen
        self.win.title(title)
        self.win.resizable(width=False, height=False)  # the window is not resizable
        self.win.iconbitmap(icon)

        self.enter_countries = tk.StringVar(value="Выберите страну")  # текст для выпадающего списка
        self.coun = ['Россия', 'Украина', 'Казахстан', 'Азербайджан', 'Беларусь', 'Грузия', 'Другие регионы',
                     'Кыргызстан',
                     'Узбекистан']  # список стран
        self.radbatts_schedule = None
        self.snippet = 0  # переменная требования
        self.address = 0  # переменная адреса компании
        self.schedule = 0  # переменная график ркботы
        self.only_with_salary = False
        self.salary_with_sort = False
        self.pages = 0  # количество страниц (по 100 объявлений на каждой)
        self.regions = "0"  # список регионов
        self.cities = "0"  # список городов
        self.country_index = -1  # переменная для проверки введённого города
        self.id_town = None  # id города
        self.ent_key_word = ''  # введенное ключевое слово
        self.choose_city = tk.Label(self.win,
                                    text="Выберите страну и мегаполис, или страну, регион, а затем город из списка:",
                                    font=('Vardana', 9, 'bold'), bg="#d9feff", relief=tk.GROOVE, bd=2, anchor="w",
                                    padx=8, width=76, pady=5)  # лэйбл Выбор города:
        self.key_word = tk.Label(self.win,
                                 text="Введите ключевую фразу или слово:", anchor="w", padx=8,
                                 font=('Vardana', 9, 'bold'), bg="#d9feff", relief=tk.GROOVE, bd=2,
                                 width=32, pady=5)  # лэйбл Ввод ключевого слова
        self.hideshow_info = tk.Label(self.win,
                                      text="Показать/Скрыть информацию:",
                                      font=('Vardana', 9, 'bold'), bg="#d9feff", relief=tk.GROOVE, bd=2, anchor="w",
                                      padx=8, width=37, pady=5)  # лэйбл Выбор города:
        self.sort_by_schedule = tk.Label(self.win,
                                         text="Показать вакансии с указанным графиком работы, либо с указанной зарплатой:",
                                         font=('Vardana', 9, 'bold'), bg="#d9feff", relief=tk.GROOVE, bd=2, anchor="w",
                                         padx=8, width=76, pady=5)  # лэйбл Выбор города:
        self.sort_by_salary = tk.Label(self.win,
                                       text="Сортировать по заработной плате:",
                                       font=('Vardana', 9, 'bold'), bg="#d9feff", relief=tk.GROOVE, bd=2, anchor="w",
                                       padx=8, width=34, pady=5)  # лэйбл Выбор города:
        self.country = Combobox(self.win, textvariable=self.enter_countries, values=(sorted(self.coun)),
                                state="readonly")  # выподающий список выбора города
        # ex_img = Pilimage.open("resourses/exit.png")  # Кнопка выхода с рисунком
        # ex_img = ex_img.resize((70, 30), Pilimage.ANTIALIAS)
        # self.exit_img = ImageTk.PhotoImage(ex_img)
        # self.exit = tk.Button(self.win, image=self.exit_img, width=70, height=30, bd=3,
        # command=self.win.destroy).place(x=910, y=56) # кнопка закрытия окна
        rep_img = Pilimage.open("resourses/replay.png")  # Кнопка повтрора с рисунком
        rep_img = rep_img.resize((70, 32), Pilimage.ANTIALIAS)
        self.replay_img = ImageTk.PhotoImage(rep_img)
        self.replay_but = tk.Button(self.win, image=self.replay_img, width=70, height=32, bd=3,
                                    command=self.replay).place(x=490, y=405)
        self.but_town_del = tk.Button(self.win, text="удалить", font=('Arial', 9, "bold"), command=self.town_delete,
                                      bg="#dae0e8", relief=tk.RAISED, bd=3, width=9,
                                      height=1)  # кнопка удаления выбранного города
        self.show_vacancies = tk.Button(self.win, text="СПИСОК\nВАКАНСИЙ", bg="#dae0e8", width=12,
                                        font=('Arial', 10, "bold"), bd=3, command=self.window_show_vacancies)

        self.key_word_entry = tk.Entry(self.win, justify=tk.CENTER, font=('Arial', 9), width=32, bg="white",
                                       relief=tk.SUNKEN,
                                       bd=2)  # entry Ввод ключевого слова
        self.key_word_butt = tk.Button(self.win, text="принять", font=('Arial', 9, "bold"), command=self.get_key_word,
                                       bg="#dae0e8", relief=tk.RAISED, bd=3, width=9,
                                       height=1)  # кнопка удаления выбранного города
        self.ivr_schedule = tk.IntVar()  #
        self.schedule_ch = tk.Checkbutton(self.win, text="График работы", command=self.schedule_get,
                                          variable=self.ivr_schedule)  # галочкa график работы
        self.ivr_address = tk.IntVar()
        self.address_ch = tk.Checkbutton(self.win, text="Адрес", command=self.address_get,
                                         variable=self.ivr_address)  # галочкa Адрес
        self.ivr_snippet = tk.IntVar()
        self.snippet_ch = tk.Checkbutton(self.win, text="Требования", command=self.snippet_get,
                                         variable=self.ivr_snippet)  # галочкa Требования

        self.ivr_salary = tk.IntVar()
        self.salary_ch = tk.Checkbutton(self.win, text="По наиболее ходовой валюте", command=self.salary_get,
                                        variable=self.ivr_salary)  # галочкa Требования
        self.choice_ivr = tk.IntVar(value=0)  # int переменная для переключателей

    def run(self):
        self.widgets()
        self.win.mainloop()  # зацикливаем окно

    def replay(self):  # обновление окна
        command = self.win.destroy()
        wind = HeadHunter()
        wind.run()


if __name__ == "__main__":
    wind = HeadHunter()
    wind.run()
