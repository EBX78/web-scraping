import pymysql                  # connect sql server
import requests                 # requests for site data
from bs4 import BeautifulSoup   # readability of site data
from unidecode import unidecode # persian number format to latin format

# connect to database, create cursor, the command for insert data to database
cnx = pymysql.connect(user = 'root', password = '795L_5795l_5', host = '127.0.0.1', database = 'abdullah')
cursor = cnx.cursor()
sql = 'INSERT INTO perfume VALUES ("%s", "%s", "%s", "%s", "%s")'

# remove strings from price integer
def PRICE(price_text):
    List = price_text.text.split()
    shits = ["تومان", "از"]
    for shit in shits:
        if shit in List:
            List.remove(shit)

    return unidecode(List[0].replace(",", ""))

# type of items(perfumes), inserted to database (All) & existing counter (existing)
par, edp, edt, edc, none, All, existing = 1, 2, 3, 4, 0, 0, 0

# start and finish in page N
s_page = int(input("START IN: "))
e_page = int(input("FINISH IN: "))

# for each page
while s_page != e_page:
    print(f"PAGE:{s_page}")
    # request site data, read site data, find item names, find items price
    response = requests.get("https://rojashop.com/shop/fragrances/eudoclon?sub=eudoclon&page=%d"% s_page)
    soup = BeautifulSoup(response.text, "html.parser")
    name = soup.find_all("strong", attrs = {"class" : "ptitle"})
    price = soup.find_all("span", attrs = {"class" : "sale-price"})

    # perfumes in page {s_page}
    for i, item in enumerate(name):
        # sent variable is for find type and sex in items, item counter
        sent = item.text
        All += 1

        try:
            # cleaning price value, existing counter
            r_price = PRICE(price[i])
            existing += 1
        except IndexError:
            r_price = "---"

        # par
        if "ادو" not in sent and "پرفیوم" in sent:
            cursor.execute(sql % (sent, par, 1, s_page, r_price)) if "مردانه" in sent else cursor.execute(sql % (sent, par, 2, s_page, r_price)) if "زنانه" in sent else cursor.execute(sql % (sent, par, 0, s_page, r_price))

        # edp
        elif "ادو" in sent and "پرفیوم" in sent:
            cursor.execute(sql % (sent, edp, 1, s_page, r_price)) if "مردانه" in sent else cursor.execute(sql % (sent, edp, 2, s_page, r_price)) if "زنانه" in sent else cursor.execute(sql % (sent, edp, 0, s_page, r_price))

        # edt
        elif "ادو" in sent and "تویلت" in sent:
            cursor.execute(sql % (sent, edt, 1, s_page, r_price)) if "مردانه" in sent else cursor.execute(sql % (sent, edt, 2, s_page, r_price)) if "زنانه" in sent else cursor.execute(sql % (sent, edt, 0, s_page, r_price))

        # edc
        elif "ادو" in sent and "کلون" in sent:
            cursor.execute(sql % (sent, edc, 1, s_page, r_price)) if "مردانه" in sent else cursor.execute(sql % (sent, edc, 2, s_page, r_price)) if "زنانه" in sent else cursor.execute(sql % (sent, edc, 0, s_page, r_price))

        # none
        else:
            cursor.execute(sql % (sent, none, 1, s_page, r_price)) if "مردانه" in sent else cursor.execute(sql % (sent, none, 2, s_page, r_price)) if "زنانه" in sent else cursor.execute(sql % (sent, none, 0, s_page, r_price))

        # excute to database
        cnx.commit()
    s_page += 1

cnx.close()
print(f'ALL: {All}\nEXISTING: {existing}')