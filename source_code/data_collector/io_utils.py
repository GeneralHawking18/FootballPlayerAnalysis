import json
import pandas as pd
import os

current_path = os.path.dirname(os.path.realpath(__file__)) + '/data/'
os.chdir(current_path)

def to_json(data, file_name = 'json_file'):
    with open('./json_data/{}.json'.format(file_name), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def to_csv(df, file_name = 'csv_file'):
    df.to_csv(r'./csv_stats/{}.csv'.format(file_name), index = None)


def read_json(file_name = 'categories'):
    with open('./json_data/{}.json'.format(file_name), 'r+') as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    print(current_path)