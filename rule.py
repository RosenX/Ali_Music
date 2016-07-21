#coding=utf-8

from const import *
from evaluate import evaluate

def Arima():
    train_set = pd.read_csv(DATA_DIR + '/train_set.csv', parse_dates=['play_time'])
    test_set = pd.read_csv(DATA_DIR + '/test_set.csv', parse_dates=['play_time'])

    train_set = train_set[train_set['play_time'] >= pd.to_datetime('20150610', format='%Y%m%d')]

    artist_play_times_train = train_set.groupby([train_set['artist_id'],
                                                 train_set['play_time'].apply(lambda x: x.date()),
                                                 train_set['type']]).count()['play_time'].xs(1, level='type')
    artist_play_times_test = test_set.groupby([test_set['artist_id'],
                                               test_set['play_time'].apply(lambda x: x.date()),
                                               test_set['type']]).count()['play_time'].xs(1, level='type')

    artist_play_times_test = DataFrame(artist_play_times_test)
    artist_play_times_test.rename(columns = {'play_time': 'real_playtimes'}, inplace = True)
    # mean_list = artist_play_times_train.groupby(level=0).mean()
    mean_list = artist_play_times_train.groupby(level=0).\
                agg(lambda x: x.median() if x.median() <= 2*x.min() else x.min())

    mean_list = artist_play_times_train.groupby(level=0).\
                agg(lambda x: x.median()-(x.median()-x.min())*0.35)

    mean_list = artist_play_times_train.groupby(level=0).\
                agg(lambda x: np.random.randint(x.median()-(x.median()-x.min())*0.5, x.median()-(x.median()-x.min())*0.1))


    time_delta_1d = pd.Timedelta('1 days')

    for artist in mean_list.index:
        new_data = artist_play_times_test.loc[artist]
        if len(artist_play_times_test.loc[artist]) < 61:
            dates = artist_play_times_test.loc[artist].index
            for i in range(1, len(dates)):
                if dates[i]-dates[i-1] > time_delta_1d: artist_play_times_test.\
                                                        loc[(artist, dates[i-1]+time_delta_1d),'real_playtimes'] =\
                                                        artist_play_times_test.loc[(artist, dates[i-1]), 'real_playtimes']

            artist_play_times_test.sort_index(level=1, inplace = True)

        new_data = artist_play_times_train.loc[artist]
        new_data = new_data.apply(lambda x: float(x))
        new_data.index = pd.Index(map(lambda x: pd.to_datetime(x, format='%Y-%m-%d'), new_data.index))

        new_data_diff = new_data.diff(1)

        arima = sm.tsa.ARMA(new_data_diff[1:],(1,0)).fit()
        start_date = artist_play_times_test.loc[artist].index[0]
        end_date = artist_play_times_test.loc[artist].index[-1]
        start_date = ''.join(str(start_date).split('-'))
        end_date = ''.join(str(end_date).split('-'))

        predict = arima.predict(start_date, end_date, dynamic=True)
        predict = list(predict)

        for i in range(0, len(predict)):
            if i == 0: predict[i] = new_data[-1] + predict[i]
            else: predict[i] = predict[i] + predict[i-1]

        artist_play_times_test.loc[artist, 'predict_playtimes'] = np.array(predict)

        # artist_play_times_test.loc[artist,'predict_playtimes'] = int(mean_list.loc[artist])
        # artist_play_times_test.loc[artist].plot(figsize=(10,6))
        # new_data = artist_play_times_test.loc[artist]
        # new_data['artist_id'] = artist
        # new_data.set_index('artist_id')
        # F1, B, P = evaluate(new_data)
        # plt.title('F1: %f  B: %f  P:%f'%(F1, B, P))
        # plt.savefig(PIC_DIR + '/predict/%s.png'%artist, dpi=300)
        # plt.show()

    evaluate(artist_play_times_test)

def MedianRule():
    train_set = pd.read_csv(RULE_TRAIN_SET, parse_dates = ['play_time'])
    test_set = pd.read_csv(RULE_TEST_SET, parse_dates = ['play_time'])

    train_set = train_set[train_set['play_time'] >= pd.to_datetime('20150620', format='%Y%m%d')]
    predict_set = test_set[test_set['play_time'] >= pd.to_datetime('20150820', format='%Y%m%d')]

    median_list = train_set.groupby('artist_id').agg(lambda x: (x.median()+x.min())/2)['play']

    test_set.set_index(['artist_id', 'play_time'], inplace= True)
    test_set.rename(columns = {'play': 'real_playtimes'}, inplace = True)

    for artist in median_list.index:
        test_set.loc[artist, 'predict_playtimes'] = int(median_list[artist])

    evaluate(test_set)

    median_list = predict_set.groupby(['artist_id']).median()['play']

    result = DataFrame()
    for artist in median_list.index:
        start = pd.to_datetime('20150901', format='%Y%m%d')
        end = pd.to_datetime('20151030', format='%Y%m%d')
        dates = pd.date_range(start ,end)
        artists = [artist]*len(dates)
        df = pd.DataFrame(artists, columns=['artist_id'])
        df['playtimes'] = int(median_list.loc[artist])
        df['date'] = dates
        result = result.append(df)

    result.to_csv(DATA_DIR + '/mars_tianchi_artist_plays_predict.csv',\
                        index=False, header=False, date_format = "%Y%m%d")

def SegMedianRule():
    train_set = pd.read_csv(DATA_DIR + '/train_set.csv', parse_dates=['play_time'])
    test_set = pd.read_csv(DATA_DIR + '/test_set.csv', parse_dates=['play_time'])

    train_set = train_set[train_set['play_time'] >= pd.to_datetime('20150301', format='%Y%m%d')]

    artist_play_times_train = train_set .groupby([train_set['artist_id'],
                                                 train_set['play_time'].apply(lambda x: x.date()),
                                                 train_set['type']]).count()['play_time'].xs(1, level='type')
    artist_play_times_test = test_set.groupby([test_set['artist_id'],
                                               test_set['play_time'].apply(lambda x: x.date()),
                                               test_set['type']]).count()['play_time'].xs(1, level='type')

    artist_list = list(artist_play_times_train.index.levels[0])

    for artist in artist_list:
        tmp = artist_play_times_train.loc[artist]
        if len(tmp) < 122:
            tmp_series = pd.DataFrame(data = [(artist, pd.to_datetime('20150519', format='%Y%m%d').date(), 5),
                                              (artist, pd.to_datetime('20150522', format='%Y%m%d').date(), 4),
                                              (artist, pd.to_datetime('20150609', format='%Y%m%d').date(), 5)],
                                      columns = ['artist_id', 'play_time'])
            tmp_series = tmp_series.set_index(['artist_id', 'play_time'])
            print tmp_series
            print artist_play_times_train.head(10)
            artist_play_times_train.append(tmp_series)
            # artist_play_times_train.loc[(artist, pd.to_datetime('20150519', format='%Y%m%d').date())] = 5
            # artist_play_times_train.loc[(artist, pd.to_datetime('20150522', format='%Y%m%d').date())] = 4
            # artist_play_times_train.loc[(artist, pd.to_datetime('20150609', format='%Y%m%d').date())] = 5
            for date in tmp.index:
                print '%s %d'%(date, artist_play_times_train.loc[(artist, date)])


    # for artist in artist_list:
    #     tmp = artist_play_times_train.loc[artist]

def testRule():
    train_set = pd.read_csv(DATA_DIR + '/train_behavior_stat.csv', parse_dates = ['play_time'])
    test_set = pd.read_csv(DATA_DIR + '/test_behavior_stat.csv', parse_dates = ['play_time'])

    train_set = train_set[train_set['play_time'] >= pd.to_datetime('20150620', format='%Y%m%d')]
    predict_set = test_set[test_set['play_time'] >= pd.to_datetime('20150820', format='%Y%m%d')]

    median_list = train_set.groupby('artist_id').agg([np.max, np.min])['play']

    # test_set.set_index(['artist_id', 'play_time'], inplace= True)
    test_set.rename(columns = {'play': 'real_playtimes'}, inplace = True)

    test_set['predict_playtimes'] = 0
    for artist in median_list.index:
        max_F = -100
        line = -1
        for i in range(int(median_list.ix[artist, 'amin']), int(median_list.ix[artist, 'amax']+1)):
            test_set.loc[test_set['artist_id']==artist, 'predict_playtimes'] = i
            F = evaluate(test_set[test_set['artist_id']==artist], out=False)
            if F > max_F:
                max_F = F
                line = i
        print (max_F, line)
        test_set.loc[test_set['artist_id']==artist, 'predict_playtimes'] = line
    evaluate(test_set, out=True)


if __name__ == '__main__':
    # testRule()
    MedianRule()
    # SegMedianRule()
    # SongMedianRule()
