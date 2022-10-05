import pymysql                  # connect sql server
import requests                 # requests for site data
from bs4 import BeautifulSoup   # readability of site data
import re                       # find required item from tag text
from unidecode import unidecode # persian number format to latin format

def PRICE(txt):                 # remove str from price
    a = txt.text.split()
    x = "از"
    y = "تومان"
    a.remove(x) if x in a else True;
    a.remove(y) if y in a else True;
    return unidecode(a[0])

cnx = pymysql.connect(user = 'root', password = '795L_5795l_5', host = '127.0.0.1', database = 'abdullah')  # connect to database
cursor = cnx.cursor()                                                                                       # create cursor
sql = 'INSERT INTO perfume VALUES ("%s", "%s", "%s", "%s", "%s")'                                           # the command for insert data to database

s_page = int(input("START IN: "))       # start in page N
e_page = int(input("FINISH IN: "))      # finish in page N

par = 1     # type of items(perfume)
edp = 2
edt = 3
edc = 4
none = 0

selected = 0    # inserted item to database
existing = 0    # count existing

# for each page
while s_page != e_page:
    response = requests.get("https://rojashop.com/shop/fragrances/eudoclon?sub=eudoclon&page=%d"% s_page)   # request data
    print("PAGE:%d"% s_page)                                                                                # print page number
    soup = BeautifulSoup(response.text, "html.parser")                                                      # readable site data
    name = soup.find_all("strong", attrs = {"class" : "ptitle"})                                            # find items name
    price = soup.find_all("span", attrs = {"class" : "sale-price"})                                         # find items price
    i = 0                                                                                                   # index counter for PRICE (line 45)

    for item in name:       # name of all perfume in s_page
        sent = item.text        # sent variable for find type and sex for items (names)

        try:
            r_price = PRICE(price[i])   # price value in (i) index (price line 38)
            existing += 1               # count existing
        except IndexError:
            r_price = "---"             # ... if price value not exist in (i) index (price line 38)
        finally:
            i += 1                      # next index

        if "ادو" in sent and "تویلت" in sent:                               # type
            if "مردانه" in sent:                                            # sex
                cursor.execute(sql % (sent, edt, 1, s_page, r_price))       # execute and insert data
            elif "زنانه" in sent:
                cursor.execute(sql % (sent, edt, 2, s_page, r_price))
            else:
                cursor.execute(sql % (sent, edt, 0, s_page, r_price))


        elif "ادو" in sent and "پرفیوم" in sent:
            if "مردانه" in sent:
                cursor.execute(sql % (sent, edp, 1, s_page, r_price))
            elif "زنانه" in sent:
                cursor.execute(sql % (sent, edp, 2, s_page, r_price))
            else:
                cursor.execute(sql % (sent, edp, 0, s_page, r_price))


        elif "ادو" not in sent and "پرفیوم" in sent:
            if "مردانه" in sent:
                cursor.execute(sql % (sent, par, 1, s_page, r_price))
            elif "زنانه" in sent:
                cursor.execute(sql % (sent, par, 2, s_page, r_price))
            else:
                cursor.execute(sql % (sent, par, 0, s_page, r_price))


        elif ("کلون" in sent and "ادو" in sent) or ("کلون" in sent):
            if "مردانه" in sent:
                cursor.execute(sql % (sent, edc, 1, s_page, r_price))
            elif "زنانه" in sent:
                cursor.execute(sql % (sent, edc, 2, s_page, r_price))
            else:
                cursor.execute(sql % (sent, edc, 0, s_page, r_price))


        elif "مردانه" in sent:
            cursor.execute(sql % (sent, none, 1, s_page, r_price))
        elif "زنانه" in sent:
            cursor.execute(sql % (sent, none, 2, s_page, r_price))
        else:
            cursor.execute(sql % (sent, none, 0, s_page, r_price))

        cnx.commit()                                                        # run execute
        selected += 1                                                       # count items
    s_page += 1                                                             # next page

cnx.close()
print("ALL:  %d"%selected)
print("EXISTING:  %d"%existing)
