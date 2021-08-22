import requests
import json
import tkinter as tk
from tkinter.ttk import Combobox
from PIL import Image as Pilimage  # для изменения размера изображения установить Pillow в pip
from PIL import ImageTk  # преобразовывает изображение из PIL для tkinter
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox as mb


class HeadHunter:
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
        # self.exit = tk.Button(self.win, image=self.exit_img, width=70, height=30, bd=3, command=self.win.destroy).place(
        #     x=910, y=56) # кнопка закрытия окна
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

    def widgets(self):  # прорисовка виджетов
        self.choose_city.place(x=20, y=10)  # лэйбл Выбор города:
        self.hideshow_info.place(x=20, y=170)  # лэйбл Показать/скрыть информацию
        self.sort_by_salary.place(x=312, y=170)  # лэйбл Сортировать по заработной плате
        self.sort_by_schedule.place(x=20, y=250)  # лэйбл только с выбранным графиком работы
        self.key_word.place(x=20, y=110)  # лэйбл Ввод ключевого слова
        self.key_word_entry.place(x=264, y=118)  # entry Ввод ключевого слова
        self.key_word_butt.place(x=494, y=110)  # кнопка подтверждения ключевого слова
        self.but_town_del.place(x=495, y=42)  # кнопка удаления города
        self.show_vacancies.place(x=242, y=400)  # кнопка показа вакансий
        self.country.place(x=20, y=50)  # выпадающий список страны
        self.schedule_ch.place(x=20, y=200)  # галочкa график работы
        self.address_ch.place(x=140, y=200)  # галочкa Адрес
        self.snippet_ch.place(x=210, y=200)  # галочкa Требования
        self.salary_ch.place(x=330, y=200)  # галочка сортировка по з/п
        self.country.bind("<<ComboboxSelected>>", self.get_country)  # отдаём выбранное значение списка стран
        tk.Radiobutton(self.win, text="Все", variable=self.choice_ivr, value=0, command=self.choice_fun).place(x=20, y=280) # переключатели
        tk.Radiobutton(self.win, text="Полный день", variable=self.choice_ivr, value=1, command=self.choice_fun).place(x=75, y=280)  # fullDay
        tk.Radiobutton(self.win, text="Удаленная работа", variable=self.choice_ivr, value=2, command=self.choice_fun).place(x=185, y=280)  # remote
        tk.Radiobutton(self.win, text="Сменный график", variable=self.choice_ivr, value=3, command=self.choice_fun).place(x=320, y=280)  # shift
        tk.Radiobutton(self.win, text="Гибкий график", variable=self.choice_ivr, value=4, command=self.choice_fun).place(x=450, y=280)  # flexible



    def get_country(self, event):  # получаем список регионов, создаем лэйблы городов
        value = self.country.get()  # сохраняем выбранное значение страны
        index = self.coun.index(value)  # индекс страны в списке
        self.country_index = index  # индекс в атрибут класса
        self.regions = [self.areas[index]["areas"][i]["name"] for i in
                        range(len(self.areas[index]["areas"]))]  # получаем список регионов
        # изменяющаяся надпись в выподающем списке
        if index == 2 or index == 3 or index == 5 or index == 7 or index == 8:
            self.enter_city = tk.StringVar(value="город")  # текст для выпадающего списка
            self.city_in_regions_text = tk.StringVar(value="")
        elif index == 0 or index == 1 or index == 4 or index == 6:
            self.enter_city = tk.StringVar(value="регион / мегаполис")  # другой текст для выпадающего списка
            # изменяющийся текст Лэйбла извещение о наличии городов
            if index == 0:
                self.city_in_regions_text = tk.StringVar(value="        Мегаполис:  Москва, Санкт-Петербург")
            elif index == 1:
                self.city_in_regions_text = tk.StringVar(value="Мегаполис:  Киев")
            elif index == 4:
                self.city_in_regions_text = tk.StringVar(value='''      Мегаполис:  Брест, Витебск,
        Гомель, Гродно, Минск, Могилев''')
            elif index == 6:
                self.city_in_regions_text = tk.StringVar(value='''Регионы:  Молдавия, Пакистан,
                Южная Осетия''')
        self.city_in_regions = tk.Label(self.win, textvariable=self.city_in_regions_text, font=("Arial", 8, "normal"),
                                        width=40, height=2).place(x=122, y=72)  # Лэйбл извещение о наличии городов
        self.reg = Combobox(self.win, textvariable=self.enter_city, values=(sorted(self.regions)), state="readonly")
        self.reg.place(x=180, y=50)  # выпадающий список регионов
        self.reg.bind("<<ComboboxSelected>>", self.get_region)  # отдаём выбранное значение списка регионов

    def get_region(self, event):
        city = self.reg.get()  # сохраняем выбранное значение региона
        for i in range(len(self.areas[self.country_index]["areas"])):  # если выбран город, передаем его id
            if self.areas[self.country_index]["areas"][i]["name"] == city and len(
                    self.areas[self.country_index]["areas"][i]["areas"]) == 0:
                id = self.areas[self.country_index]["areas"][i]["id"]
                self.get_city(id, self.areas[self.country_index]["areas"][i]["name"])  # передаем id и название города
                break
            elif self.areas[self.country_index]["areas"][i]["name"] == city and len(
                    self.areas[self.country_index]["areas"][i]["areas"]) != 0:  # если регион, получаем список городов
                self.cities = [self.areas[self.country_index]["areas"][i]["areas"][j]["name"] for j in
                               range(len(self.areas[self.country_index]["areas"][i]["areas"]))]
                self.num_region = i
                self.enter_town = tk.StringVar(value="Выберите город")
                self.town = Combobox(self.win, textvariable=self.enter_town, values=(sorted(self.cities)),
                                     state="readonly")
                self.town.place(x=338, y=50)
                self.town.bind("<<ComboboxSelected>>", self.get_town)  # отдаём выбранное значение списка городов
                break

    def get_city(self, id, city):  # метод записи id города из 2-го выпадающего списка
        self.choose_city["bg"] = "#5ad136"  # меняем цвет лэйбла на зеленый
        self.choose_city["fg"] = "white"
        self.choose_city.place()
        self.but_town_del["bg"] = "#5ad136"  # меняем цвет кнопки удаления на зеленый
        self.but_town_del["fg"] = "white"
        self.but_town_del.place()
        self.id_town = id
        self.found_num_if_vacancies()

    def get_town(self, event):  # метод получения города из 3-го выпадающего списка
        town = self.town.get()
        try:
            for i in self.areas[self.country_index]["areas"][self.num_region]["areas"]:
                if i["name"] == town:
                    self.choose_city["bg"] = "#5ad136"  # меняем цвет лэйбла на зеленый
                    self.choose_city["fg"] = "white"
                    self.choose_city.place()
                    self.but_town_del["bg"] = "#5ad136"  # меняем цвет кнопки удаления на зеленый
                    self.but_town_del["fg"] = "white"
                    self.but_town_del.place()
                    self.id_town = i["id"]
                    self.found_num_if_vacancies()
                    break
        except Exception:
            mb.showinfo("Предупреждение", "Выберите другой регион")

    def town_delete(self):  # кнопка удаления города
        self.choose_city["bg"] = "#d9feff"  # меняем цвет лэйбла на первоначальный
        self.choose_city["fg"] = "black"
        self.choose_city.place()
        self.but_town_del["bg"] = "#dae0e8"  # меняем цвет кнопки удаления на первоначальный
        self.but_town_del["fg"] = "black"
        self.but_town_del.place()
        self.id_town = None
        self.found_num_if_vacancies()

    def get_key_word(self):  # подтверждаем ключевое слова и запускаем функцию подсчета вакансий
        self.ent_key_word = self.key_word_entry.get()
        if len(self.ent_key_word) > 0:
            self.key_word["bg"] = "#5ad136"  # меняем цвет дэйбла на зеленый
            self.key_word["fg"] = "white"
            self.key_word.place()
            self.key_word_butt["bg"] = "#5ad136"  # меняем цвет кнопки подтверждения на зеленый
            self.key_word_butt["fg"] = "white"
            self.key_word_butt.place()
            self.found_num_if_vacancies()  # запускаем функцию подсчета вакансий
        elif len(self.ent_key_word) == 0:
            self.key_word["bg"] = "#d9feff"  # меняем цвет лэйбла на первоначальный
            self.key_word["fg"] = "black"
            self.key_word.place()
            self.key_word_butt["bg"] = "#dae0e8"  # меняем цвет кнопки подтверждения на первоначальный
            self.key_word_butt["fg"] = "black"
            self.key_word_butt.place()
            self.ent_key_word = ''
            self.found_num_if_vacancies()  # запускаем функцию подсчета вакансий

    def found_num_if_vacancies(self):  # нахождение количества вакансий
        url = "https://api.hh.ru/vacancies"
        number_of_pages = {
            'text': self.ent_key_word,  # Текст фильтра
            'area': self.id_town,  # Поиск ощуществляется по вакансиям города
            'per_page': 100,  # Кол-во вакансий на 1 странице
            'page': 0,  # Индекс страницы поиска на HH
            'only_with_salary': self.only_with_salary,
            'schedule': self.radbatts_schedule
        }
        req = requests.get(url, number_of_pages)
        data = req.content.decode()
        req.close()
        page_vacancy = json.loads(data)
        self.pages = page_vacancy["pages"]
        num_vac = str(page_vacancy["found"])  # количество найденных вакансий
        found_num_vac = tk.StringVar(
            value=f"Найдено вакансий: {num_vac}")  # текст для лйбла - количество найденных вакансий
        tk.Label(self.win, textvariable=found_num_vac, font=('Vardana', 10, 'bold'), relief=tk.GROOVE, bd=2, height=2,
                 width=23).place(x=202, y=360)  # лэйбл количество найденных вакансий

    def window_show_vacancies(self):  # создание окна списка вакансий
        self.vac_win = tk.Tk()
        self.vac_win.geometry(f"1600x600+50+50")  # size and padding of the window on screen
        self.vac_win.title("Найденные вакансии")
        self.vac_win["bg"] = "#e8e6da"  # background color
        self.vac_win.iconbitmap("resourses/hh.ico")
        self.vac_win.resizable(width=False, height=False)
        self.st = ScrolledText(self.vac_win,
                               width=195,
                               height=38,
                               bg="#f5f5f5",
                               fg="#8c8c8c",
                               selectbackground="black",
                               selectforeground="white",
                               font=("Verdana", 10),
                               padx=10,
                               pady=5,
                               state=tk.DISABLED,  # только для чтения и большинство методов, как insert, не сработают
                               wrap=tk.WORD,  # перенос по словам, по умолчанию стоит посимвольный
                               spacing2=5,  # отступ между строками текста в пикселях
                               )
        self.st.configure(state=tk.NORMAL)
        self.st.pack()  # прокрутка текста
        self.st.tag_config("vac")
        n = 1
        self.l_with_salary = []
        salary_rur = []
        for i in range(self.pages):
            url = "https://api.hh.ru/vacancies"
            number_of_pages = {
                'text': self.ent_key_word,  # Текст фильтра
                'area': self.id_town,  # Поиск ощуществляется по вакансиям города
                'per_page': 100,  # Кол-во вакансий на 1 странице
                'page': i,  # Индекс страницы поиска на HH
                'only_with_salary': self.only_with_salary,  # по умолчанию False вакансии с указанной З.П.
                'schedule': self.radbatts_schedule
            }
            req = requests.get(url, number_of_pages)
            data = req.content.decode()
            req.close()
            page_vacancy = json.loads(data)
            if self.salary_with_sort:  # если сортировка включена
                try:
                    for j in range(len(page_vacancy["items"])):
                        self.l_with_salary.append([])  # создаём вложенный список
                        # self.l_with_salary[-1].append(page_vacancy["items"][j]["salary"]["currency"])
                        if page_vacancy["items"][j]["salary"]["to"] != None:
                            # записываем в [[0]] индекс зарплату по ключу to
                            self.l_with_salary[-1].append(page_vacancy["items"][j]["salary"]["to"])
                        else:  # иначе по ключу from
                            self.l_with_salary[-1].append(page_vacancy["items"][j]["salary"]["from"])
                        self.l_with_salary[-1].append(str(n) + ". ")  # отступ
                        for key, value in page_vacancy["items"][j].items():  # открываем словарь вакансии
                            if key == "name":  # Если ключ - имя вакансии(должжность) вставляем её
                                self.l_with_salary[-1].append(str(value) + "   ")
                            elif key == "salary" and value != None:  # если зарплата указана, вставляем ОТ, ДО, ВАЛЮТА
                                if value["from"] != None and value["to"] == None:
                                    salary_rur.append(value["currency"])
                                    self.l_with_salary[-1].append("з/п: от " + str(value["from"]) +
                                                                  " " + value["currency"] + "   ")
                                elif value["from"] == None and value["to"] != None:
                                    salary_rur.append(value["currency"])
                                    self.l_with_salary[-1].append("з/п: до " + str(value["to"]) +
                                                                  " " + value["currency"] + "   ")
                                elif value["from"] != None and value["to"] != None:
                                    salary_rur.append(value["currency"])
                                    self.l_with_salary[-1].append("з/п: от " + str(value["from"])
                                                                  + " до " + str(value["to"]) +
                                                                  " " + value["currency"] + "   ")
                            elif key == "address" and value != None and self.address != 0:  # адрес компании
                                if value["raw"] != None:
                                    self.l_with_salary[-1].append("Адрес: " + value["raw"] + "   ")
                            elif key == "alternate_url":
                                self.l_with_salary[-1].append("URL: " + str(value) + "   ")
                            elif key == "snippet" and value != None and self.snippet != 0:  # требования к соискателю
                                if value["requirement"] != None:
                                    self.l_with_salary[-1].append("Требования: " +
                                                                  value["requirement"] + "   ")
                            elif key == "schedule" and value != None and self.schedule != 0:  # график работы
                                self.l_with_salary[-1].append("График работы: " + value["name"] + "   ")
                        self.l_with_salary[-1].append(salary_rur[-1])
                        n += 1
                except Exception:
                    pass
            else:  # если сортировка отключена
                try:
                    for j in range(len(page_vacancy["items"])):
                        self.st.insert(tk.INSERT, str(n) + ". ", "vac")  # номер вакансии
                        for key, value in page_vacancy["items"][j].items():
                            if key == "name":  # Если ключ - имя вакансии(должжность) вставляем её
                                self.st.insert(tk.INSERT, str(value) + "   ", "vac")
                            elif key == "salary" and value != None:  # если зарплата указана, вставляем ОТ, ДО, ВАЛЮТА
                                if value["from"] != None and value["to"] == None:
                                    self.st.insert(tk.INSERT,
                                                   "з/п: от " + str(value["from"]) + " " + value["currency"] + "   ",
                                                   "vac")
                                elif value["from"] == None and value["to"] != None:
                                    self.st.insert(tk.INSERT,
                                                   "з/п: до " + str(value["to"]) + " " + value["currency"] + "   ",
                                                   "vac")
                                elif value["from"] != None and value["to"] != None:
                                    self.st.insert(tk.INSERT,
                                                   "з/п: от " + str(value["from"]) + " до " + str(value["to"]) + " " +
                                                   value["currency"] + "   ", "vac")
                            elif key == "address" and value != None and self.address != 0:  # адрес компании
                                if value["raw"] != None:
                                    self.st.insert(tk.INSERT, "Адрес: " + value["raw"] + "   ", "vac")
                            elif key == "alternate_url":
                                self.st.insert(tk.INSERT, "URL: " + str(value) + "   ", "vac")
                            elif key == "snippet" and value != None and self.snippet != 0:  # требования к соискателю
                                if value["requirement"] != None:
                                    self.st.insert(tk.INSERT, "Требования: " + value["requirement"] + "   ", "vac")
                            elif key == "schedule" and value != None and self.schedule != 0:  # график работы
                                self.st.insert(tk.INSERT, "График работы: " + value["name"] + "   ", "vac")
                        self.st.insert(tk.INSERT, "\n\n", "vac")
                        n += 1
                except Exception:
                    pass
        try:
            if self.salary_with_sort:  # если сортировка включена, сортируем полученный ранее список
                most_common_rur = max(salary_rur, key=salary_rur.count)  # находим наиболее ходовую валюту
                self.l_with_salary = sorted(self.l_with_salary, reverse=True)  # сортировка от max до min
                n = 0  # вырезая и вставляя в конец элементы списка, исправляем нумерацию последовательности
                for g in range(len(self.l_with_salary)):
                    if self.l_with_salary[g - n][-1] != most_common_rur:
                        # если валюта в данном элементе не ходовая, отправляем её в конец списка
                        self.l_with_salary.append(self.l_with_salary.pop(g - n))
                        n += 1
                for g in range(len(self.l_with_salary)):
                    for h in range(len(self.l_with_salary[g])):
                        if h != 0 and h != (
                                len(self.l_with_salary[g]) - 1):  # выводим всё кроме 1 и последнего элемента
                            self.st.insert(tk.INSERT, self.l_with_salary[g][h], "vac")
                    self.st.insert(tk.INSERT, "\n\n", "vac")
        except Exception:
            pass
        self.st.configure(state=tk.DISABLED)
        self.vac_win.bind("<FocusOut>", self.on_focus_in)  # если окно теряет фокус, закрываем его
        self.vac_win.mainloop()  # Зацикливаем окно списка вакансий

    def on_focus_in(self, event):  # если окно теряет фокус, закрываем окно
        if event.widget == self.vac_win:
            command = self.vac_win.destroy()

    def schedule_get(self):  # показать/скрыть график работы
        if self.ivr_schedule.get():
            self.schedule = 1
        else:
            self.schedule = 0
        if self.address == 1 and self.snippet == 1 and self.schedule == 1:  # если нажаты все галочки
            self.hideshow_info["bg"] = "#5ad136"  # меняем цвет лэйбла на зелёный
            self.hideshow_info["fg"] = "white"
        else:
            self.hideshow_info["bg"] = "#d9feff"  # меняем цвет лэйбла на первоначальный
            self.hideshow_info["fg"] = "black"

    def snippet_get(self):  # показать/скрыть требования
        if self.ivr_snippet.get():
            self.snippet = 1
        else:
            self.snippet = 0
        if self.address == 1 and self.snippet == 1 and self.schedule == 1:  # если нажаты все галочки
            self.hideshow_info["bg"] = "#5ad136"  # меняем цвет лэйбла на зелёный
            self.hideshow_info["fg"] = "white"
        else:
            self.hideshow_info["bg"] = "#d9feff"  # меняем цвет лэйбла на первоначальный
            self.hideshow_info["fg"] = "black"

    def address_get(self):  # показать/скрыть адрес
        if self.ivr_address.get():
            self.address = 1
        else:
            self.address = 0
        if self.address == 1 and self.snippet == 1 and self.schedule == 1:  # если нажаты все галочки
            self.hideshow_info["bg"] = "#5ad136"  # меняем цвет лэйбла на зелёный
            self.hideshow_info["fg"] = "white"
        else:
            self.hideshow_info["bg"] = "#d9feff"  # меняем цвет лэйбла на первоначальный
            self.hideshow_info["fg"] = "black"

    def salary_get(self):
        if self.ivr_salary.get():
            self.only_with_salary = True
            self.salary_with_sort = True
            self.sort_by_salary["bg"] = "#5ad136"  # меняем цвет лэйбла на зелёный
            self.sort_by_salary["fg"] = "white"
            self.found_num_if_vacancies()
        else:
            self.only_with_salary = False
            self.salary_with_sort = False
            self.sort_by_salary["bg"] = "#d9feff"  # меняем цвет лэйбла на первоначальный
            self.sort_by_salary["fg"] = "black"
            self.found_num_if_vacancies()

    def choice_fun(self):
        choise_get = self.choice_ivr.get()
        if choise_get == 0:
            self.radbatts_schedule = None
            self.sort_by_schedule["bg"] = "#d9feff"  # меняем цвет лэйбла на первоначальный
            self.sort_by_schedule["fg"] = "black"
            self.found_num_if_vacancies()
        if choise_get == 1:
            self.radbatts_schedule = 'fullDay'
            self.sort_by_schedule["bg"] = "#5ad136"  # меняем цвет лэйбла на зелёный
            self.sort_by_schedule["fg"] = "white"
            self.found_num_if_vacancies()
        if choise_get == 2:
            self.radbatts_schedule = 'remote'
            self.sort_by_schedule["bg"] = "#5ad136"  # меняем цвет лэйбла на зелёный
            self.sort_by_schedule["fg"] = "white"
            self.found_num_if_vacancies()
        if choise_get == 3:
            self.radbatts_schedule = 'shift'
            self.sort_by_schedule["bg"] = "#5ad136"  # меняем цвет лэйбла на зелёный
            self.sort_by_schedule["fg"] = "white"
            self.found_num_if_vacancies()
        if choise_get == 4:
            self.radbatts_schedule = 'flexible'
            self.sort_by_schedule["bg"] = "#5ad136"  # меняем цвет лэйбла на зелёный
            self.sort_by_schedule["fg"] = "white"
            self.found_num_if_vacancies()


    def replay(self):  # обновление окна
        command = self.win.destroy()
        wind = HeadHunter()
        wind.run()


if __name__ == "__main__":
    wind = HeadHunter()
    wind.run()
