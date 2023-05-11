import datetime
import requests
from bs4 import BeautifulSoup
import xlwt
import xlrd
from xlutils.copy import copy
from datetime import date
import re
import pandas as pd

# set the search range for last 10 years.
img_data = []

player_data = []

season = ["34173", "30249", "27725", "24346", "21029", "18527", "9224", "2254", "934", "527", "525"]

player_list = []

today = date.today()


def set_xls_name(stat_type):
    # xls doc set
    book_name_xls = 'Player ' + stat_type + '.xls'
    return book_name_xls


def set_sheet_name(split):
    sheet_name_xls = split
    return sheet_name_xls


def write_excel_xls(path, sheet_name, value):
    index = len(value)  # Gets the number of rows to write data
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(sheet_name)
    for i in range(0, index):
        sheet.write(0, i, value[i])  # Write data (corresponding rows and columns) to a table
    workbook.save(path)
    print("Different Team Data Add.")


def write_excel_xls_append(path, value):
    index = len(value)
    workbook = xlrd.open_workbook(path)
    sheets = workbook.sheet_names()  # Gets all the sheets in the workbook
    worksheet = workbook.sheet_by_name(sheets[0])  # Gets the first sheet
    rows_old = worksheet.nrows  # Get the existed rows in the sheet
    new_workbook = copy(workbook)  # Converts a copy of a xlrd object to a xlwt object
    new_worksheet = new_workbook.get_sheet(0)  # Gets the first sheet in the transformed workbook
    for i in range(0, index):
        for o in range(0, len(value[i])):
            new_worksheet.write(i + rows_old, o, value[i][o])  # add data from i+rows_old lines
    new_workbook.save(path)
    print('Total lines is : ' + index.__str__())
    print("xls doc complete")


def img_data_append(data_list, first_size):
    chunk_size = first_size
    for i in range(0, len(data_list), chunk_size):
        img_data.append(data_list[i:i + chunk_size])
    return img_data


# grab the player information page url and grab the data of date of birth
def get_player_url_date(url):
    res = requests.get(url).text
    content = BeautifulSoup(res, "html.parser")
    # get the data for head and each teams
    main = content.find_all('main')
    for m in main:
        img = m.find('div', class_="mt-12 block lg:h-120 w-1/2 lg:w-full lg:absolute h-full bg-full-h-auto bg-top "
                                   "bg-no-repeat")
        img_url = img['style'].replace('background-image:', '').replace('url(', '').replace(')', '').replace('?;', '')
        if img_url == "/images/person-placeholder.svg":
            img_url = "https://nbl.com.au/images/person-placeholder.svg"
        check = m.find('div', class_="row flex flex-wrap py-3 border-b border-gray-accent-200 text-sm")

        if check is not None:
            check_birthday = m.find('div', class_="w-1/3 text-gray-accent-500")
            if check_birthday.text.strip() == "Date of Birth":
                for div in check.find('div', class_="w-2/3 font-bold pl-5"):
                    divs = div.text.strip().replace(',', '').split()
                    day = re.findall(r"\d+", divs[0])
                    day = day[0]
                    month = divs[1]
                    year = divs[2]
                    b = day + '/' + month + '/' + year
                    b1 = datetime.datetime.strptime(b, "%d/%B/%Y").date()
                    age = today.year - b1.year - ((today.month, today.day) < (b1.month, b1.day))
                    return img_url, age
            else:
                return img_url, 'Unknown'
        else:
            return img_url, 'Unknown'


def get_selected_data(csv):
    csv_name = csv + '.csv'
    dt = pd.read_csv(csv_name)
    dt_name = dt['Player'].values.tolist()

    for x in season:
        url = 'https://nbl.com.au/stats/all-time?season={}'.format(x)
        print(url)
        res = requests.get(url).text
        content = BeautifulSoup(res, "html.parser")
        # get the data for head and each teams
        main = content.find_all('main')

        # Find selected data by analysing html tags
        for m in main:
            for a in m.find_all('a', class_="flex-1 leading-none text-sm lg:text-base font-proxima-bold font-bold "
                                            "align-middle py-3 px-3"):
                href = a['href']
                player = a.text.strip()
                if player not in player_list:
                    if player in dt_name:
                        index = dt[dt['Player'] == player].index.values
                        print(index)

                        player_list.append(player)
                        full_url = ('https://nbl.com.au' + href)
                        img_url = get_player_url_date(full_url)[0]
                        age = get_player_url_date(full_url)[1]
                        dt.loc[index, ('Img', 'Age')] = [[img_url, age]]
                        print(player + ' age is : ' + str(age) + ' ' + img_url)

    print('Complete')


# !!!!!if want to use different types of data just change the tags below!!!!
get_selected_data('DimPlayer')
