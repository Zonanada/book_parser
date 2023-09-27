from general import BrowserOzon, isbn_keywords, isbn_anti_keywords, little_pause
from selenium.webdriver.common.by import By
from database import Database
import random
import re

class ParsePageOzon(BrowserOzon):
    def __init__(self, links: list, city, driver):
        self.city = city
        self.driver = driver
        self.links = links
        self.db = Database()
        self.iterate_all_links()
    
    def iterate_all_links(self):
        for isbn in self.links:
            self.isbn = isbn
            for link in self.links[isbn]:
                try:
                    try:
                        self.parse_page(link)
                    except:
                        print("EXCEPT!!!")
                        self.parse_page(link)
                except Exception as e: 
                    print(e)
                    print("DATA LOSS!!!")
        self.driver.close()

    def parse_page(self, product_url):
        self.driver.get(product_url)
        little_pause()
        try:
            self.driver.find_element(By.XPATH, "//span[text()='Подтвердите возраст']")
            self.driver.find_element(By.CSS_SELECTOR, "input").send_keys("15.11.1988")
            little_pause()
            self.driver.find_element(By.XPATH, "//span[text()='Подтвердить']").click()
        except:
            pass

        self.wait_loaded("XPATH", "//div[@data-widget='webCharacteristics']")
        self.driver.execute_script(f"window.scrollTo(0, {random.randint(300,500)})")
        self.wait_loaded("XPATH", "//div[@data-widget='webCurrentSeller']")
        parameters = self.driver.find_elements(By.XPATH, "//div[@data-widget='webCharacteristics']")[1].text
        parameters += self.driver.find_element(By.XPATH, "//div[@data-widget='webProductHeading']").text
        if (self.is_have_keywords(parameters)):
            seller_info = self.driver.find_element(By.XPATH, "//div[@data-widget='webCurrentSeller']")
            seller = seller_info.text.split('\n')[1]
            price_info = self.driver.find_element(By.XPATH, "//div[@data-widget='webPrice']").text.split("\n")[0]
            price = self.str_to_int(price_info)
            self.db.add_product(self.isbn, price, seller, self.city, "Ozon")
            print(f"ADD => {product_url}")


    def is_have_keywords(self, parameters: str) -> bool:
        for word in isbn_keywords[self.isbn]:
            search = re.search(fr'{word}', parameters)
            if (search == None):
                return False
        for word in isbn_anti_keywords[self.isbn]:
            search = re.search(fr'{word}', parameters)
            if (search != None):
                return False
        return True


    def str_to_int(self, str):
        result = list()
        for num in range(len(str)):
            if (str[num].isdigit()):
                result.append(str[num])
        return int(''.join(result))