import requests
from bs4 import BeautifulSoup
import time
import xlwt
import xlrd
from xlutils.copy import copy
import pymssql

conn = pymssql.connect(host="127.0.0.1", user="lei", password="123456", database="Wildcats", charset="cp936")

if conn:
    print("success")

c1 = conn.cursor()

c1.execute('SELECT * FROM DimPlayer')
print(c1.fetchall())

# set the search range for last 10 years.
year = time.localtime().tm_year
year_range = 12
year_list = []
col = 0
row = 0

# Set the year list for last 10 years
for k in range(year_range):
    reduceYear = year - k
    year_list.append(reduceYear)
print(year_list)

# set the Stat Type
stat_Type = ['Averages', 'Totals', 'Per_48', 'Per_40', 'Per_36', 'Per_Minute', 'Misc_Stats', 'Advanced_Stats']

# set the Split
split_Type = ['Team_Totals', 'Team_Starters', 'Team_Bench', 'Opponent_Totals', 'Opponent_Starters', 'Opponent_Bench']

new_data = []


def set_xls_name(stat_type):
    # xls doc set
    book_name_xls = '12 years data with ' + stat_type + '.xls'
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
    print("Data header add.")


def write_excel_xls_append(path, value):
    index = len(value)
    workbook = xlrd.open_workbook(path)
    sheets = workbook.sheet_names()  # Gets all the sheets in the workbook
    worksheet = workbook.sheet_by_name(sheets[0])  # Gets the first sheet
    rows_old = worksheet.nrows  # Get the existed rows in the sheet
    new_workbook = copy(workbook)  # Converts a copy of a xlrd object to a xlwt object
    new_worksheet = new_workbook.get_sheet(0)  # Gets the first sheet in the transformed workbook
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i + rows_old, j, value[i][j])  # add data from i+rows_old lines
    new_workbook.save(path)
    print('Total lines is : ' + index.__str__())
    print("xls doc complete")


def new_data_append(data_list, first, second, years):
    chunk_size = 22
    for i in range(0, len(data_list), chunk_size):
        new_data.append(data_list[i:i + chunk_size])

    for o in range(second - first, second):
        new_data[o][0] = [years.__str__()]
    return new_data


def get_selected_data(y, z, second=0):
    for x in year_list:
        url = 'https://basketball.realgm.com/international/league/5/Australian-NBL/team-stats/{}/{}/{}'.format(x, y, z)
        res = requests.get(url).text
        content = BeautifulSoup(res, "html.parser")
        # get the data for head and each teams
        table = content.find_all('table')
        head_list = []
        data_list = []

        # Find selected data by analysing html tags
        for t in table:
            h_list = t.find_all('th')
            tm_list = t.find_all('td')
            for u in tm_list:
                data_list.append(u.string)
            for h in h_list:
                head_list.append(h.string)
        head_list[0] = ['Year']
        write_excel_xls(set_xls_name(y), set_sheet_name(z), head_list)

        # calculate each for loop new data list length
        length = (data_list.__len__() / 22).__int__()
        first = length
        second += length
        print(first.__str__() + " new lines. ", second.__str__() + ' Total lines')
        new_data_append(data_list, first, second, x)

        print('successful add ' + x.__str__() + "'s" + ' Stat Type: ' + y + '. Split by: ' + z)
    return new_data


# !!!!!if want to use different types of data just change the tags below!!!!
write_excel_xls_append(set_xls_name('Totals'), get_selected_data('Totals', 'Team_Totals'))
