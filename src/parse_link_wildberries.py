from general import little_pause
from general import medium_pause
from selenium.webdriver.common.by import By
from general import BrowserWildberries

isbns_names = {9785996616534: "ЛЕГИОН ЕГЭ 2023 Русский язык 25 тренировочных вариантов", 
         9785996615971: "ЛЕГИОН ЕГЭ 2023 математика 40 тренировочных вариантов", 
         9785996617388: "Русский язык. ЕГЭ-2024. Тематический тренинг. Модели сочинений. 10-11 классы",
         9785996617197: "ЛЕГИОН ЕГЭ 2024 Русский язык 25 тренировочных вариантов",
         9785996617562: "ЛЕГИОН ОГЭ Математика 2024 40 тренировочных вариантов",
         9785996617623: "Математика. Подготовка к ЕГЭ-2024. Профильный уровень. 40 тренировочных вариантов по демоверсии 2024 года"}



class ParseLinksWildberries(BrowserWildberries):
    def __init__(self, city, isbns):
        super().__init__(city)
        self.all_links = dict()
        self.select_city(self.city)
        for isbn in isbns:
            url = self.generate_url(isbns_names[isbn])
            self.parse_link(url, isbn, isbns_names[isbn])

    def generate_url(self, url:str):
        result = ""
        for word in url.split(" "):
            result += word + "%20"
        return f"https://www.wildberries.ru/catalog/0/search.aspx?search={result}"
        

    def parse_link(self, url, isbn, isbns_name):
        self.driver.get(url)
        self.wait_loaded("CLASSNAME", "searching-results__title")
        little_pause()
        if isbns_name in self.driver.find_element(By.CLASS_NAME, "searching-results__title").text:
            scrol_to = 1000
            for _ in range(6):
                medium_pause()
                self.driver.execute_script(f"window.scrollTo(0, {scrol_to})")
                scrol_to+=1000
            
            links = list()
            self.wait_loaded("XPATH", "//div[@class='product-card-list']")
            products = self.driver.find_element(By.XPATH, "//div[@class='product-card-list']").find_elements(By.CSS_SELECTOR, "a")
            for id, product in enumerate(products):
                if (id % 2 == 0):
                    url = product.get_attribute('href')
                    links.append(url)
            self.all_links[isbn] = links


    def get_links(self):
        return self.all_links

    def get_driver(self):
        return self.driver