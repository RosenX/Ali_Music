#coding=utf-8

from const import *
from evaluate import evaluate

def other_evaluate(filename):
    predict = pd.read_csv(filename, names=['artist_id', 'real_playtimes', 'predict_playtimes'])
    evaluate(predict)

def rf_result(filename):
    f = open(filename, 'r')
    result = pd.DataFrame()
    for line in f:
        line = line.split(',')
        start = pd.to_datetime('20150901', format='%Y%m%d')
        end = pd.to_datetime('20151030', format='%Y%m%d')
        dates = pd.date_range(start ,end)
        artists = line[0]
        artists = [artists]*len(dates)
        playtimes = map(lambda x: int(float(x)), line[1:])
        df = pd.DataFrame(artists, columns=['artist_id'])
        df['playtimes'] = playtimes
        df['date'] = dates
        result = result.append(df)

    result.to_csv('mars_tianchi_artist_plays_predict.csv',
                        index=False, header=False, date_format = "%Y%m%d")

if __name__ == '__main__':
    # other_evaluate("submit.csv")
    rf_result('result4.csv')
