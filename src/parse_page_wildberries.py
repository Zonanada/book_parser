from general import BrowserWildberries, isbn_keywords, isbn_anti_keywords
from selenium.webdriver.common.by import By
from database import Database
import re


class ParsePageWildberries(BrowserWildberries):
    def __init__(self, links: list, city, driver):
        self.driver = driver
        self.links = links
        self.db = Database()
        self.city = city
        self.iterate_all_links()

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

    def get_price(self, price_info):
        for num in price_info:
            num_int = self.str_to_int(num.text)
            if (num_int):
                return num_int

    def parse_page(self, product_url):
        self.driver.get(product_url)
        self.wait_loaded("XPATH", "//ins[@class='price-block__final-price']")
        price_info = self.driver.find_elements(By.XPATH, "//ins[@class='price-block__final-price']")
        price = self.get_price(price_info)

        self.driver.execute_script("window.scrollTo(0, 800)")
        self.wait_loaded("XPATH", "//div[@class='seller-info__title']")

        seller = self.driver.find_element(By.XPATH, "//div[@class='seller-info__title']").text
        try:
            self.driver.find_element(By.XPATH, "//button[contains(text(),'Развернуть характеристики')]").click()
        except:
            pass
        parameters = self.driver.find_element(By.XPATH, "//div[@class='details-section__details details-section__details--about details']").text
        if (self.is_have_keywords(parameters)):
            self.db.add_product(self.isbn, price, seller,self.city, "Wildberries")
            print(f"ADD => {product_url}")

    def str_to_int(self, str):
        if (len(str) == 0):
            return None
        result = list()
        for num in range(len(str)):
            if (str[num].isdigit()):
                result.append(str[num])
        return int(''.join(result))

    def __dell__(self):
        self.driver.close()