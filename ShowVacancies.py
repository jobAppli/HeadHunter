from tkinter.scrolledtext import ScrolledText
import tkinter as tk
import requests
import json

class ShowVacancies:

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
                'area': self.id_town,  # Поиск осуществляется по вакансиям города
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