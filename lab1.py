# Комар Анастасія, ФБ-11

import pandas as pd
import urllib
from datetime import datetime
import glob
import warnings

warnings.filterwarnings("ignore")

path = r'C:\Users\Lenovo\Desktop\4 семестр\зпад\lab_1'


# завантаження даних
def get_data():
    i = 1
    while i < 28:
        now = datetime.now()
        date_time_string = now.strftime("%d-%m-%Y_%H-%M")
        filename = 'vhi_id_{}_{}.csv'.format(i, date_time_string)
        url='https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1=1981&year2=2023&type=Mean'.format(i)
        vhi_url = urllib.request.urlopen(url)
        out=open(filename, 'wb')
        out.write(vhi_url.read())
        out.close()
        print("Файл для {} області створено.".format(i))
        i += 1

        
# створення датафрейму
def dataframe(path):
    headers = ['year', 'week', 'smn', 'smt', 'vci', 'tci', 'vhi', 'empty']
    headers_usecols = ['year', 'week', 'smn', 'smt', 'vci', 'tci', 'vhi']
    all_files = glob.glob(path + "/vhi_id*.csv")
    li = []
    i = 1
    for filename in all_files:
        df = pd.read_csv(filename, index_col = None, header = 1, names = headers, usecols = headers_usecols)
        df = df.drop(df.loc[df['vhi'] == -1].index)
        df = df.dropna()
        df['area'] = i
        li.append(df)
        i = i + 1
    
    frame = pd.concat(li, axis = 0, ignore_index = True) 
    return frame


# зміна індексів
def index_change(frame):
    old_index = 1
    indices = ["22", "24", "23", "25", "3", "4", "8", "19", "20", "21", "9", "26", "10", "11", "12", "13", "14", "15", "16", "27", "17", "18", "6", "1", "2", "7", "5"]
    # 26 - Київ, 27 - Севастополь
    for new_index in indices:
        frame["area"].replace({old_index:new_index}, inplace = True)
        old_index += 1
    frame.to_csv('vhi_full.csv')
    print("Індекси були змінені")


# ряд VHI для області за рік, пошук екстремумів (min та max)
def area_in_year_vhi(frame, area, year):
    vhi_list = []
    frame_vhi = frame[(frame["area"] == area) & (frame["year"] == year)]
    for i in frame_vhi["vhi"]:
        vhi_list.append(i)

    print(f'{"*"*91}')
    print(f'Ряд VHI в області з індексом {area} за {year} рік: {vhi_list}')
    print("Максимальне значення: {}".format(frame_vhi["vhi"].max()))
    print("Мінімальне значення: {}".format(frame_vhi["vhi"].min()))
    print(f'{"*"*91}')

    
# Ряд VHI за всі роки для області, виявити роки з екстремальними/помірними
# посухами, які торкнулися більше вказаного відсотка області
def dry_years(area, percent, vhi_content):
    frame_vhi = frame[frame["area"] == area]
    years = []
    unfavorable_years = []
    
    for i in frame_vhi["year"]:
        if i not in years:
            years.append(i)
    
    for year in years:
        unfavorable_weeks = 0 
        frame_years = frame_vhi[frame["year"] == year]
        weeks = len(frame_years)
        
        for j in frame_years["vhi"]:    
            if j < vhi_content:
                unfavorable_weeks += 1
                
        #print(f'{year} - {unfavorable_weeks} - {weeks}')    
        maths = (unfavorable_weeks/weeks)*100
        #print(f'% of the area: {maths}')
        if maths > percent:
            unfavorable_years.append(year)
    print(f'Несприятливими роками є: {unfavorable_years}')

    
answ = input("Отримати дані?(так/ні) ")
if answ == "так" or answ == "Так":
    get_data()

frame = dataframe(path)
    
answ = input("Змінити індекси?(так/ні) ")
if answ == "так" or answ == "Так":    
    index_change(frame)
    
answ = input("Провести аналіз даних?(так/ні) ")
if answ == "так" or answ == "Так":
    area = int(input("Введіть індекс області: "))
    year = str(input("Введіть рік (з 1981 по 2023):"))
    percent = int(input("Введіть відсоток: "))
    vhi_content = int(input(" 15 - екстремальні посухи (<15)\n 35 - помірні посухи (<35)\nВкажіть, яка посуха вас цікавить:"))
    
    area_in_year_vhi(frame, area, year)
    dry_years(area, percent, vhi_content)