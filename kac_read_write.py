import sys
import json
import urllib3
import certifi
import numpy as np
import pandas as pd
from pandas import Series,DataFrame, read_html

p = lambda x: print(x)

def read_csv_as_df(name, header=0, nrows=None):
    """Return DataFrame from file\n
    IN: \n
    (str) name = name of file\n
    (int) header = which row is a header (None if none of it) \n
    (int) nrows = how many rows download from file (None if all)
    
    OUT: \n
    Return Automated Index DataFrame
    """
    return pd.read_csv(name, header=header, nrows=nrows)

def read_csv_as_df2(name, sep=',', header=0):
    """Return DataFrame from file\n
    IN: \n
    (str) name = name of file\n
    (str) sep = separator between data \n
    (int) header = which row is a header (None if none of it) \n
    
    OUT: \n
    Return Automated Index DataFrame
    """
    return pd.read_table(name, sep=sep, header=header)

def write_df_to_csv(df, name, sep=',', columns=None):
    """Save DataFrame to file\n
    IN: \n
    (str) name = name of file\n
    (DataFrame) df = dataframe \n
    (char) sep = which char should separate items \n
    (list) columns = which columns do you want to save (None if all)

    OUT: \n
    Return nothing - save dataframe to file
    """
    df.to_csv(name, sep=sep, columns=columns)
    
def json_to_dict(json_obj):
    """Convert json to dict\n
    IN: \n
    (json) json_obj = name of json file\n

    OUT: \n
    Return dict \n
    """
    return json.loads(json_obj)

def dict_to_json(dict_obj):
    """Convert dict to json\n
    IN: \n
    (dict) dict_obj = name of dict file/var\n

    OUT: \n
    Return json \n
    """
    return json.dumps(dict_obj)

def web_to_df(url):
    """Downloads all table from html of url\n
    IN: \n
    (str) url = name of the website \n

    OUT: \n
    Return list of DataFrames (if there are many tables) \n
    """
    https = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where(),)  
    url = https.urlopen('GET',url) 
    return pd.read_html(url.data)

def xlsx_to_df(name, sheet_name='Sheet1', header=0, index_col=None):
    """Download sheet to dataframe\n
    IN: \n
    (str) name = name of Excel file \n
    (str) sheet_name = name of the sheet which should be parse \n
    (int) header = Row (0-indexed) to use for the column labels of the parsed DataFrame (None if not) \n
    (int) index_col = Column (0-indexed) to use as the row labels of the DataFrame.

    OUT: \n
    Return list of DataFrames (if there are many tables) \n
    """
    xlsxfile = pd.ExcelFile(name)
    return xlsxfile.parse(sheet_name=sheet_name, header=header, index_col=index_col)

def df_to_xlsx(df,file_name, sheet_name='Sheet(1)'):
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name)
    
def add_df_to_exist_xlsx(df, file_name, sheet_name='Sheet(1)'):

    # read a single or multi-sheet excel file
    # (returns dict of sheetname(s), dataframe(s))
    ws_dict = pd.read_excel(file_name, sheet_name=None)

    # easy to change a worksheet as a dataframe:
    # mod_df = ws_dict['existing_worksheet']

    # do work on mod_df...then reassign
    #ws_dict['existing_worksheet'] = mod_df

    # add a dataframe to the workbook as a new worksheet with
    # ws name, df as dict key, value:
    ws_dict[sheet_name] = df

    # when done, write dictionary back to excel...
    # xlsxwriter honors datetime and date formats
    with pd.ExcelWriter(file_name,
                        engine='xlsxwriter',
                        datetime_format='yyyy-mm-dd',
                        date_format='yyyy-mm-dd') as writer:

        for ws_name, df_sheet in ws_dict.items():
            df_sheet.to_excel(writer, sheet_name=ws_name)


# Test nr1 - read write text files
#df = read_csv_as_df('lec25.csv',header=None)
#df = read_csv_as_df2('lec25.csv',sep=',',header=None)
#write_df_to_csv(df,'mytextdata_out.csv')
#p(df)


# Test n2 - read
# json_obj = """
# {   "zoo_animal": "Lion",
#     "food": ["Meat", "Veggies", "Honey"],
#     "fur": "Golden",
#     "clothes": null, 
#     "diet": [{"zoo_animal": "Gazelle", "food":"grass", "fur": "Brown"}]
# }
# """
# p(json_obj)
# # Json to dict
# data = json_to_dict(json_obj)
# p(data)
# # Back to json
# json_obj2 = dict_to_json(data)
# p(json_obj2)

# df = DataFrame(data['diet'])
# p(df)



# Test nr3 - read write html
# url = 'https://www.bankier.pl/gielda/notowania/akcje/PZU/podstawowe-dane'#'http://www.fdic.gov/bank/individual/failed/banklist.html'
# #dframe_list = pd.io.html.read_html(url)
# dframe_list = web_to_df(url)
# dframe = dframe_list[0]


# dframe

# dframe.columns.values


# Test nr4 - read write excel files
#####
#
# pandas.pydata.org/pandas-docs/dev/generated/pandas.io.excel.ExcelFile.parse.html
#
#####
# xlsfile = pd.ExcelFile('Lec_28_test.xlsx')
# dframe = xlsx_to_df('Lec_28_test.xlsx', header=0)
# p(dframe)
# add_df_to_exist_xlsx(df=dframe, file_name='Lec_28_test.xlsx', sheet_name='Test')

