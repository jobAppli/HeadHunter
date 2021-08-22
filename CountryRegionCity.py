from tkinter import messagebox as mb
import tkinter as tk
from tkinter.ttk import Combobox


class CountryRegionCity:

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

