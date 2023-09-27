from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def little_pause():
    sleep(2)

def medium_pause():
    sleep(4)

def big_pause():
    sleep(6)


class Browser:
    def __init__(self, city):
        self.city = city
        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'eager'
        options.add_argument("window-size=1920,1080")
        options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
        '''})

    def wait_loaded(self, type, adds:str):
        if (type == "XPATH"):
            element_present = EC.presence_of_element_located((By.XPATH, adds))
        else:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, adds))
        WebDriverWait(self.driver, 30).until(element_present)



class BrowserWildberries(Browser):
    def select_city(self, city):
        print(f"start select sity Wildberries : {city}")
        if (city == "Москва"):
            return
        self.driver.get("https://www.wildberries.ru/")
        if (city == "Ростов-на-Дону"):
            set_city = "Ростов-на-Дону, 3-Я Баррикадная Улица 2"
        else:
            set_city = city
        little_pause()
        self.wait_loaded("XPATH", "//span[text()='Москва']")
        self.driver.find_element(By.XPATH, "//span[text()='Москва']").click()
        self.wait_loaded("XPATH", "//input[@placeholder='Введите адрес']")
        self.driver.find_element(By.XPATH, "//input[@placeholder='Введите адрес']").send_keys(f"{set_city}")
        self.wait_loaded("XPATH", "//*[contains(text(), 'Найти')]")
        self.driver.find_element(By.XPATH, "//*[contains(text(), 'Найти')]").click()
        medium_pause()
        self.wait_loaded("CLASS", "address-item__name")
        self.driver.find_element(By.CLASS_NAME,  "address-item__name").click()
        self.wait_loaded("XPATH", "//div[@class='details-self__btn-wrap']//button[@type='button']")
        little_pause()
        self.driver.find_element(By.XPATH, "//div[@class='details-self__btn-wrap']//button[@type='button']").click()
        medium_pause()
        print("finish select sity wildberries")

    def __dell__(self):
        self.driver.close()
    

            
class BrowserOzon(Browser):
    def select_city(self, city):
        print(f"start select sity Ozon : {city}")
        self.driver.get("https://www.ozon.ru/")
        medium_pause()
        self.wait_loaded("XPATH", "//span[text()='Укажите адрес доставки']")
        self.driver.find_element(By.XPATH, "//span[text()='Укажите адрес доставки']").click()
        self.wait_loaded("XPATH", "//span[text()='Изменить']")
        self.driver.find_element(By.XPATH, "//span[text()='Изменить']").click()
        self.wait_loaded("XPATH", "//input[@type='search']")
        self.driver.find_element(By.XPATH, "//input[@type='search']").send_keys(f"{city}")
        self.wait_loaded("XPATH", f"//div[text()='{city}']")
        self.driver.find_element(By.XPATH, f"//div[text()='{city}']").click()
        print("finish select sity ozon")


    def __dell__(self):
        self.driver.close()



isbn_keywords = {9785996616534: ["Сенина", "ЕГЭ"],
                 9785996615971: ["Лысенко", "Кулабухов", "ЕГЭ"],
                 9785996617388: ["Сенина", "ЕГЭ", "Гармаш"],
                 9785996617197: ["Сенина"],
                 9785996617562: ["Лысенко", "Иванов", "ОГЭ"],
                 9785996617623: ["Лысенко", "Кулабухова", "ЕГЭ"]}

isbn_anti_keywords = {9785996616534: ["Литература"],
                 9785996615971: ["Базовый уровень"],
                 9785996617388: [],
                 9785996617197: [],
                 9785996617562: [],
                 9785996617623: []}
