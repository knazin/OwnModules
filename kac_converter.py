import kac_read_write as krw
import json
import time
import os

def CSVtoJSON(csvfile, delimiter):
    os.system('clear')

    #df = krw.(csvfile,header=0)
    #print(df)
    file = open(csvfile, 'r')
    lines = file.read().split('\n')
    filej = open(csvfile.split('.')[0]+'.json', 'w')
    jsonfile = []
    for line in lines[1:]:
        jsonfile.append(
            {
                'lat': line.split(delimiter)[0].replace(',','.'),
                'lng': line.split(delimiter)[1].replace(',','.')
            }
        )
    filej.write(json.dumps(jsonfile))
    filej.close()
    print('File converted')

if __name__ == "__main__":
    CSVtoJSON('data/telepizza2.csv',';')
        
    