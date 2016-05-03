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

def dataAnalyse():
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
            plt.savefig(PIC_DIR+'/%d.png'%(i/5+1), dpi=300)
    plt.show()


if __name__ == '__main__':
    #dataStat()
    dataAnalyse()
