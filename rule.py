#coding=utf-8

from const import *
from evaluate import evaluate

def mean_rule_1():
    train_set = pd.read_csv(DATA_DIR + '/train_set.csv', parse_dates=['play_time'])
    test_set = pd.read_csv(DATA_DIR + '/test_set.csv', parse_dates=['play_time'])

    artist_action_times_train = train_set.groupby([train_set['artist_id'],
                                            train_set['play_time'].apply(lambda x: x.date()),
                                            train_set['type']]).count()['play_time']
    artist_action_times_test = test_set.groupby([test_set['artist_id'],
                                          test_set['play_time'].apply(lambda x: x.date()),
                                          test_set['type']]).count()['play_time']

    artist_play_times_train = artist_action_times_train.xs(1, level='type')
    artist_play_times_test = artist_action_times_test.xs(1, level='type')

    artist_play_times_test = DataFrame(artist_play_times_test)
    artist_play_times_test.rename(columns = {'play_time': 'real_playtimes'}, inplace = True)
    mean_list = artist_play_times_train.groupby(level=0).mean()

    artist_play_times_test['predict_playtimes'] = 0
    for artist in mean_list.index:
        artist_play_times_test.loc[artist,'predict_playtimes'] = mean_list.loc[artist]
    evaluate(artist_play_times_test)


if __name__ == '__main__':
    mean_rule_1()
