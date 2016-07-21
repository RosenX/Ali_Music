#coding=utf-8

from const import *

def rule_split_data(file_in):
    action = pd.read_csv(file_in, parse_dates=['play_time'])
    split_date = pd.to_datetime('20150701',format='%Y%m%d')
    train_set = action[action['play_time'] < split_date]
    test_set = action[action['play_time'] >= split_date]
    print len(train_set)
    print len(test_set)
    train_set.to_csv(RULE_TRAIN_SET, index = False)
    test_set.to_csv(RULE_TEST_SET, index = False)


def behavior_stat(file_in, file_out):
    df = pd.read_csv(file_in, parse_dates = ['play_time'])
    # df.sort_values(by = 'play_time', inplace = True)
    group = df.groupby([df['artist_id'], df['play_time'].apply(lambda x: x.date()), df['type']])
    stat = group.count()['play_time'].unstack()
    stat.columns = ['play', 'collect', 'download']
    stat.reset_index(inplace = True)
    ## 补全
    # start_date = df.iloc[0]['play_time']
    # end_date = df.iloc[-1]['play_time']
    start_date = pd.to_datetime('20150228', format = '%Y%m%d')
    end_date = pd.to_datetime('20150830', format = '%Y%m%d')
    dates = DataFrame(pd.date_range(start_date, end_date).date, columns=['play_time'])
    stat = pd.merge(stat, dates, on='play_time', how='left')
    stat['play'].fillna(method = 'ffill', inplace = True)
    stat['collect'].fillna(method = 'ffill', inplace = True)
    stat['download'].fillna(0, inplace = True)
    # print len(stat)
    stat.to_csv(file_out, index = False)

def model_split_data(file_in):
    data = pd.read_csv(file_in, parse_dates = ['play_time'])
    data.set_index('artist_id', inplace=True)

    train_set = DataFrame()
    test_x_set = DataFrame()
    test_real_set = DataFrame()
    for i, artist in enumerate(data.index.unique()):
        train_set_sm, test_x, test_real = extractFeature(data.loc[artist])
        train_set = train_set.append(train_set_sm)
        test_x_set = test_x_set.append(test_x.T)
        test_real_set = test_real_set.append(test_real.T)
        print 'The %dth singer complete!'%(i+1)

    train_set.to_csv(MODEL_TRAIN_SET)
    test_x_set.to_csv(MODEL_TEST_X_SET, index = False)
    test_real_set.to_csv(MODEL_TEST_REAL_SET, index = False)

def calBestLine(result):
    max_F = -1
    best_line = -1
    max_playtime = result.max()
    min_playtime = result.min()
    result = DataFrame(result)
    result.rename(columns = {'play': 'real_playtimes'}, inplace = True)
    for i in range(int(min_playtime), int(max_playtime)):
        result['predict_playtimes'] = i
        F_B = evaluate(result, False)
        if F_B > max_F:
            max_F = F_B
            best_line = i
    return best_line


def extractFeature(data):
    end_date = pd.to_datetime('20150830', format='%Y%m%d')
    start_date = pd.to_datetime('20150228', format='%Y%m%d')
    period_60_day = Timedelta('60 days')
    period_1_day = Timedelta('1 days')
    period_train = Timedelta('10 days')

    # print data.head(10)
    train_set = []
    test_x = []
    test_real = []
    date_range = pd.date_range(start_date, end_date-period_60_day-period_train).date
    for i, date in enumerate(date_range):
        x_end = date + period_train
        y_end = x_end + period_60_day
        x_set = data[(data['play_time'] >= date) & (data['play_time'] < x_end)]
        y_set = data[(data['play_time'] >= x_end) & (data['play_time'] <= y_end)]
        x = list(x_set['play']) + list(x_set['collect'])
        if i == len(date_range)-1:
            test_x = x
            test_real = list(y_set['play'])
        else:
            y = calBestLine(y_set['play'])
            x.append(y)
            train_set.append(x)

    return DataFrame(train_set), DataFrame(test_x), DataFrame(test_real)

if __name__ == '__main__':
    # behavior_stat(DATA_DIR + '/new_actions.csv', DATA_DIR + '/behavior_stat.csv')
    # rule_split_data(DATA_DIR + '/behavior_stat.csv')
    model_split_data(DATA_DIR + '/behavior_stat.csv')
