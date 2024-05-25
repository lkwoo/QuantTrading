import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import col_info

def test1():
    cols = []

    with open('col_info.py', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("'") is False:
                continue
            temp = line.replace("'", "").replace(",", "").split(':')
            cols.append([temp[0].strip(), temp[1].strip()])

    for col in cols:
        print(f"{col[0].replace(' ', '_')} text,")

    for col in cols:
        print(f"comment on column stock_info.{col[0].replace(' ', '_')} is '{col[1]}';")

def test2():
    for a in col_info.col_type_mapper:
        print(a)

def test3():
    keys_list = list(col_info.col_type_mapper.keys())
    print(keys_list)

if __name__ == '__main__':
    test3()