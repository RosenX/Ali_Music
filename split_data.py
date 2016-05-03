#coding=utf-8

from const import *

def split_data():
    action = pd.read_csv(NEW_ACTIONS_FILE, parse_dates=['play_time'])
    action.sort_values(by = 'play_time', inplace = True)
    split_date = pd.to_datetime('20150701',format='%Y%m%d')
    train_set = action[action['play_time'] < split_date]
    test_set = action[action['play_time'] >= split_date]

    train_set.to_csv(DATA_DIR + '/train_set.csv', index = False)
    test_set.to_csv(DATA_DIR + '/test_set.csv', index = False)

if __name__ == '__main__':
    split_data()
