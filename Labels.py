class Labels:
    '''switch color label buttons / изменение цветов лэйблов и кнопок'''

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
        """меняем цвет переключателя 'показать скрыть информацию' и вызов функции подсчёта вакансий"""
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
        """меняем цвет переключателя 'график работы' и вызов функции подсчёта вакансий"""
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
