import csv
import os

PATH = './data.csv'

if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
    print('file exists')

else:
    with open('data.csv', 'w', newline='') as fp:
        a = csv.writer(fp, delimiter=',')
        data_head = [['name', 'pincode', 'status', 'category']]
        a.writerows(data_head)