# define css selector for pollutants buttons

AQI = "body > div.btns > ul > li:nth-child(1) > a"
PM25 = "body > div.btns > ul > li:nth-child(2) > a"
SO2 = "body > div.btns > ul > li:nth-child(3) > a"
NO2 = "body > div.btns > ul > li:nth-child(4) > a"
O3 = "body > div.btns > ul > li:nth-child(5) > a"
CO = "body > div.btns > ul > li:nth-child(6) > a"
PM10 = "body > div.btns > ul > li:nth-child(7) > a"

PULLUTANTS = {'AQI': AQI,
             'PM25': PM25,
             'SO2': SO2,
             'NO2': NO2,
             'O3': O3,
             'CO': CO,
             "PM10": PM10}

test1 = "#t_overlaysDiv > div:nth-child(30) > div > div > img"
test2 = "#t_overlaysDiv > div:nth-child(35) > div > div > img"
test3 = "#t_overlaysDiv > div:nth-child(36) > div > div > img"
#t_overlaysDiv > div:nth-child(2) > div > div > img

# define 34 air station points here

POINT_FRONT = "#t_overlaysDiv > div:nth-child"
POINT_LIST = [POINT_FRONT + "({})".format(str(i)) for i in range(2, 36)]
