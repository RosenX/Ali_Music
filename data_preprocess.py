#coding=utf-8

from const import *

def data_preprocess():
    actions = pd.read_csv(ACTIONS_FILE, names = ['user_id', 'song_id', 'play_time', 'type', 'record_time'])
    songs = pd.read_csv(SONGS_FILE, names = ['song_id', 'artist_id', 'publish_time',
                                             'song_init_plays', 'language', 'gender'])
    songs = songs[['song_id', 'artist_id']]
    actions = actions[['song_id', 'play_time', 'type']]

    ## 时间转换
    actions['play_time'] = actions.play_time.apply(lambda x: datetime.datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H'))

    ## 将必要信息加入到action中
    new_action = pd.merge(actions, songs, on='song_id')
    # new_action.sort_values(by = 'play_time', inplace = True)
    del new_action['song_id']

    print new_action.head(10)

    new_action.to_csv(NEW_ACTIONS_FILE, index = False)

if __name__ == '__main__':
    data_preprocess()
