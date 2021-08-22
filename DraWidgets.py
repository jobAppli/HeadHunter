import tkinter as tk


class DraWidgets:
    """Задаём координаты и прорисовываем виджеты"""

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
        tk.Radiobutton(self.win, text="Все", variable=self.choice_ivr,
                       value=0, command=self.choice_fun).place(x=20, y=280)  # переключатели
        tk.Radiobutton(self.win, text="Полный день", variable=self.choice_ivr, value=1, command=self.choice_fun).place(
            x=75, y=280)  # fullDay
        tk.Radiobutton(self.win, text="Удаленная работа", variable=self.choice_ivr, value=2,
                       command=self.choice_fun).place(x=185, y=280)  # remote
        tk.Radiobutton(self.win, text="Сменный график", variable=self.choice_ivr, value=3,
                       command=self.choice_fun).place(x=320, y=280)  # shift
        tk.Radiobutton(self.win, text="Гибкий график", variable=self.choice_ivr, value=4,
                       command=self.choice_fun).place(x=450, y=280)  # flexible
