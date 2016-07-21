#coding=utf-8

from const import *

def dataStat():
    df = pd.read_csv(SONGS_FILE, names = ['song_id', 'artist_id', 'publish_time'
                                        , 'song_init_plays', 'language', 'gender'])
    print 'Artist number: %d' % len(df['artist_id'].unique())
    print 'Song number: %d' % len(df['song_id'].unique())
    print 'Language number: %d' % len(df['language'].unique())
    print 'Gender number: %d' % len(df['gender'].unique())

    f = open(DATA_DIR + '/stat.txt', 'w')
    f.write('Artist number: %d\n' % len(df['artist_id'].unique()));
    f.write('Song number: %d\n' % len(df['song_id'].unique()));
    f.write('Language number: %d\n' % len(df['language'].unique()));
    f.write('Gender number: %d\n' % len(df['gender'].unique()));
    f.close();

def singerPlaytimeAnalyse():
    action = pd.read_csv(NEW_ACTIONS_FILE, parse_dates=['play_time'])
    action = action[action['type'] == 1]
    artist_group = action.groupby([action['artist_id'], action['play_time'].apply(lambda x: x.date())])
    play_times = artist_group.count()['play_time']

    artist_list = play_times.index.levels[0]

    for i in range(50):
        if i%5 == 0:
            fig, axes = plt.subplots(5, 1, figsize=(15,8))
            plt.subplots_adjust(hspace = 1)
        play_times.loc[artist_list[i]].plot(ax = axes[i%5])
        if i%5 == 4:
            plt.savefig(PIC_DIR+'/singer_%d~%d.png'%(i-3, i+1), dpi=300)
    plt.show()

def singerPlaytimeSumAnalyse():
    action = pd.read_csv(NEW_ACTIONS_FILE, parse_dates=['play_time'])
    action = action[action['type'] == 1]
    artist_group = action.groupby([action['artist_id'], action['play_time'].apply(lambda x: x.date())])
    play_times = artist_group.count()['play_time']

    artist_list = play_times.index.levels[0]

    for artist in artist_list:
        # fig, axes = plt.subplots(2, 1, figsize=(15, 12))
        # play_times.loc[artist].cumsum().plot(ax = axes[0])
        fig = plt.figure(figsize=(12, 8))
        play_times.loc[artist].diff(1).plot()
        plt.savefig(PIC_DIR + '/%s_diff_1.png'%artist, dpi=300)
        plt.show()

    # for i in range(50):
    #     if i%5 == 0:
    #         fig, axes = plt.subplots(5, 1, figsize=(15,8))
    #         plt.subplots_adjust(hspace = 1)
    #     play_times.loc[artist_list[i]].cumsum().plot(ax = axes[i%5])
    #     if i%5 == 4:
    #         plt.savefig(PIC_DIR+'/singer_sum_%d~%d.png'%(i-3, i+1), dpi=300)
    # plt.show()

def songPlaytimeAnalyse():
    action = pd.read_csv(NEW_ACTIONS_FILE, parse_dates=['play_time'])
    action = action[action['type'] == 1]
    artist_group = action.groupby([action['song_id'], action['play_time'].apply(lambda x: x.date())])
    play_times = artist_group.count()['play_time']
    mean_list = play_times.groupby(level=0).mean()
    mean_list.sort_values(ascending = False, inplace = True)

    print mean_list[0:-1:10]

# def songAnalyse():
#     action = pd.read_csv(NEW_ACTIONS_FILE, parse_dates=['play_time'])
#     action_group = action.groupby([action['song_id'],action['play_time'].apply(lambda x: x.date(), action['type'])])
#     play_times = artist_group.count()


def test():
    # train_set = pd.read_csv('train.csv', names=['artist', 'date', 'playtimes'])
    test_set = pd.read_csv('test.csv', names=['artist', 'date', 'playtimes'], parse_dates = ['date'])
    test_set = test_set[test_set['date'] < pd.to_datetime('20150711', format='%Y%m%d')]
    test_set.to_csv('part_test.csv', index = False, header = False)
    print test_set.head(10)
    print test_set.dtypes
    print len(test_set['artist'].unique())

def bestF1():
    action = pd.read_csv(NEW_ACTIONS_FILE, parse_dates=['play_time'])
    start_month = 3
    end_month = 8
    for m in range(start_month, end_month):
        start_date = pd.to_datetime("2015%d"%m, format="%Y%m")
        end_date = pd.to_datetime("2015%d"%(m+2), format="%Y%m")
        tmp = action[(action['play_time'] >= start_date) & (action['play_time'] < end_date)]
        tmp = tmp.groupby([tmp['artist_id'], tmp['play_time'].apply(lambda x: x.date()),
                           tmp['type']]).count()['play_time'].xs(1, level='type')
        tmp = tmp.groupby(level=0).agg(lambda x: math.sqrt(x.sum()))
        print "%d~%d: %f"%(m, m+1, tmp.sum())


def WorkdayAndWeekend():
    action = pd.read_csv(NEW_ACTIONS_FILE, parse_dates=['play_time'])
    stat = action.groupby([action['play_time'].apply(lambda x: int(x.strftime("%w"))), action['type']]).count()
    # stat =  action.query('type==3')['play_time'].apply(lambda x: int(x.strftime("%w")))
    # stat = stat['gender'].xs(2, level='type')
    stat = stat['gender']
    stat.plot();
    # stat.plot(kind = 'hist', alpha = 1, bins = 6);
    plt.show();


if __name__ == '__main__':
    dataStat()
    # singerPlaytimeAnalyse()
    # songPlaytimeAnalyse()
    # singerPlaytimeSumAnalyse()
    # test()
    # bestF1()
    # WorkdayAndWeekend()
