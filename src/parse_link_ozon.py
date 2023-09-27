from general import BrowserOzon
from general import little_pause
from general import medium_pause
from selenium.webdriver.common.by import By


class ParseLinksOzon(BrowserOzon):
    def __init__(self, city, isbns):
        super().__init__(city)
        self.all_links = dict()
        self.select_city(self.city)
        for isbn in isbns:
            self.parse_link(f"https://www.ozon.ru/search/?from_global=true&sorting=ozon_card_price&text={isbn}", isbn)

    def parse_link(self, url, isbn):
        print(f"parse_link => {url}")
        self.driver.get(url)
        self.wait_loaded("XPATH", "//div[@data-widget='megaPaginator']")
        scrol_to = 1000
        for _ in range(5):
            medium_pause()
            self.driver.execute_script(f"window.scrollTo(0, {scrol_to})")
            scrol_to+=1000
        products = self.driver.find_element(By.XPATH, "//div[@data-widget='megaPaginator']").find_elements(By.CLASS_NAME, 'tile-hover-target')
        links = list()
        for index, url in enumerate(products[:52]):
            if (index % 2):
                link = url.get_attribute('href').split('/?')[0]
                links.append(link)
        self.all_links[isbn] = links
        print(f"finish parse_link")

    def get_links(self):
        return self.all_links
    
    def get_driver(self):
        return self.driver