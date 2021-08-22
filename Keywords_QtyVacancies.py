import tkinter as tk
import requests
import json


class Keywords_QtyVacancies:

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