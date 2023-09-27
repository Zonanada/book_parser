from database import Database
import pandas as pd
import copy
from datetime import datetime

isbns = [9785996616534, 9785996615971, 9785996617388, 9785996617197, 9785996617562, 9785996617623]
all_city = {"Санкт-Петербург":"СПБ", "Москва":"МСК", "Ростов-на-Дону":"РНД"}

class GenerateCytyPrice():
    def __init__(self, sity, marketplace, isbn):
        self.db = Database()
        self.excel = dict()
        self.marketplace = marketplace
        self.sity = sity
        self.isbn = isbn
        self.excel[all_city[self.sity]] = []
        self.excel['Дата'] = []
        self.result = list()
        self.data_structuring()
        self.colonic_generation()
        self.write_isbn_date()
        self.write_in_excell()

    def data_structuring(self):
        data = self.db.get_data(self.sity, self.marketplace, self.isbn)
        if len(data) == 0:
            return

        isbn = data[0][1]
        date = data[0][0]
        line = list()
        for product in data:
            if (product[0] == date and product[1] == isbn):
                line.append(product)
            else:
                date = product[0]
                isbn = product[1]
                self.result.append(copy.deepcopy(line))
                line.clear()
                line.append(product)
        self.result.append(line)

    def colonic_generation(self):
        for num in range(22):
            self.excel[f"Цена {num+1}"] = []
            self.excel[f"Продавец {num+1}"] = []


    def write_isbn_date(self):
        for line in self.result:
            self.excel[all_city[self.sity]].append(f"ISBN {line[0][1]}")
            date = datetime.fromtimestamp(line[0][0]).strftime("%d.%m.%Y")
            self.excel["Дата"].append(date)


    def write_in_excell(self):
        for line in self.result:
            for num in range(22):
                if (num < len(line)):
                    self.excel[f"Цена {num+1}"].append(line[num][2])
                    self.excel[f"Продавец {num+1}"].append(line[num][3])
                else:
                    self.excel[f"Цена {num+1}"].append(" ---- ")
                    self.excel[f"Продавец {num+1}"].append(" ---- ")
    
    def get_datafreim(self):
        return pd.DataFrame(self.excel)
    

def generate_excell(marketpalce):  
    writer = pd.ExcelWriter(f"../result_parse/{marketpalce}.xlsx", engine='xlsxwriter')
    all_city_excell = dict()
    for isbn in isbns:
        for city in all_city:
            gen = GenerateCytyPrice(city, marketpalce, isbn)
            all_city_excell[f"{all_city[city]}_{str(isbn)[11:]}"] = gen.get_datafreim()
    for sheet_name in all_city_excell:
        all_city_excell[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    writer.close()