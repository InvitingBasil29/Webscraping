import requests
from bs4 import BeautifulSoup
import time
import xlwt
import xlrd
from xlutils.copy import copy


# set the search range for last 10 years.
year = time.localtime().tm_year
year_range = 12
year_list = []
col = 0
row = 0


#Season - 12 options ---
#League - Australian NBL ---
#Team - All Australian NBL Teams ---
#Stat Type - Averages, Totals, Advanced Stats (3 options) ---
#Prospects - All Prospects  ---
#Position - PG, SG, SF, PF, C (5 options) ---
#Qualified - Unticked ---
#Pace Adjusted - Ticked ---

#in total, 12 x 3 x 5 options = 180 extractions.

#There should be 3 CSV files-for each Stat Type. Each CSV file will contain data for all 12 seasons, and all positions.

#Each table will have as many columns as shown in the website PLUS 2 columns - Season and Position

# Set the year list for last 10 years
for k in range(year_range):
    reduceYear = year - k
    year_list.append(reduceYear)
print(year_list)

# set the Stat Type
stat_Type = ['Averages', 'Totals', 'Advanced_Stats']

#set the position type:
position_Type = ['PG', 'SG', 'SF', 'PF', 'C']


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



def new_data_append(data_list, first_size, years, position):
    chunk_size = first_size
    empty_list = [years.__str__(), position.__str__()]
    for i in range(1, len(data_list), chunk_size):
        new_data.append(data_list[i:i + chunk_size - 1] + empty_list)
    return new_data



def get_selected_data(y, z):
    for x in year_list:
        url = 'https://basketball.realgm.com/international/league/5/Australian-NBL/stats/{}/{}/All/All/points/{}/desc/1?pace_adjustment='.format(x, y, z)
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

        first_size = head_list.__len__()
        head_list.pop(0)
        head_list.append('Season')
        head_list.append('Position')


        write_excel_xls(set_xls_name(y), set_sheet_name(y), head_list)

        # calculate each for loop new data list length
        new_data_append(data_list, first_size, x, z)

        print('successful add ' + x.__str__() + "'s" + ' Stat Type: ' + y + '. Split by: ' + z)
    return new_data


# !!!!!if want to use different types of data just change the tags below!!!!

for j in position_Type:
    write_excel_xls_append(set_xls_name('Totals'), get_selected_data('Totals', j.__str__()))

new_data = []
for j in position_Type:
    write_excel_xls_append(set_xls_name('Averages'), get_selected_data('Averages', j.__str__()))

new_data = []
for j in position_Type:
    write_excel_xls_append(set_xls_name('Advanced_Stats'), get_selected_data('Advanced_Stats', j.__str__()))