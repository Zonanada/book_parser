from parse_link_ozon import ParseLinksOzon
from parse_page_ozon import ParsePageOzon
from parse_link_wildberries import ParseLinksWildberries
from parse_page_wildberries import ParsePageWildberries
from excel import generate_excell
from send_mail import seng_mail
from general import big_pause
from config import RECIPIENT
isbns = [9785996616534, 9785996615971, 9785996617388, 9785996617197, 9785996617562, 9785996617623]
all_city = ["Санкт-Петербург", "Москва", "Ростов-на-Дону"]

def main():
    for city in all_city:
            fail = True
            while fail:
                try:
                    parselinkozon = ParseLinksOzon(city, isbns)
                    ParsePageOzon(parselinkozon.get_links(), city, parselinkozon.get_driver())
                    fail = False
                except Exception as e:
                    print("exception Ozon!")
                    print(e)
                    big_pause()
                    

            fail = True
            while fail:
                try:
                    parselinkwildberries = ParseLinksWildberries(city, isbns)
                    ParsePageWildberries(parselinkwildberries.get_links(), city, parselinkwildberries.get_driver())
                    fail = False
                except Exception as e:
                    print("exception wildberries!")
                    print(e)
                    big_pause()


    generate_excell("Wildberries")
    generate_excell("Ozon")
    seng_mail(RECIPIENT, 'Данные с парсера Ozon/Wildberries')


if __name__ == "__main__":
    main()