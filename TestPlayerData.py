import requests
from bs4 import BeautifulSoup
import xlwt
import xlrd
from xlutils.copy import copy


# set the search range for last 10 years.
img_data = []

player_data = []

player_team_data = ["3682/adelaide-36ers", "3709/brisbane-bullets", "3713/cairns-taipans", "130770/illawarra-hawks",
                    "7694/melbourne-united", "3684/nz-breakers", "3692/perth-wildcats", "113805/se-melbourne",
                    "3694/sydney-kings", "140349/tasmania-jackjumpers"]

try_list = []


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


def get_selected_data():
    global src
    for x in player_team_data:
        url = 'https://nbl.com.au/teams/{}'.format(x)
        print(url)
        res = requests.get(url).text
        content = BeautifulSoup(res, "html.parser")
        # get the data for head and each teams
        main = content.find_all('main')

        head_list = ['Name', 'Url']
        image_list = []
        # Find selected data by analysing html tags
        for m in main:
            for h3 in m.find_all('h3', class_="lg:mt-3 text-base block font-bold xxs:text-xs xs:text-base xl:text-xl"):
                for img in m.find_all('img', class_="mr-3"):
                    src = img['src']
                t0 = h3.text.split()
                try_list.append(t0[0] + ' ' + t0[1])
                try_list.append(src)
                image_list.append(try_list[0])
                image_list.append(try_list[1])
                try_list.clear()

        first_size = head_list.__len__()
        write_excel_xls(set_xls_name("Img"), set_sheet_name('Img'), head_list)
        img_data_append(image_list, first_size)
    return img_data


# !!!!!if want to use different types of data just change the tags below!!!!
write_excel_xls_append(set_xls_name('Img'), get_selected_data())
