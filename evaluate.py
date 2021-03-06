#coding=utf-8
from const import *

def evaluate(predict_set, out=True):
    # print predict_set.head(10)
    # predict_set = predict_set.set_index('artist_id')
    predict_set['sigma'] = ((predict_set['predict_playtimes']-predict_set['real_playtimes'])/
                             predict_set['real_playtimes'])**2
    artist_group = predict_set.groupby(level=0)

    sigma = pd.DataFrame(artist_group['sigma'].apply(lambda x: math.sqrt(x.sum()/x.count())))
    sigma['phi'] = artist_group['real_playtimes'].sum().apply(lambda x: math.sqrt(x))
    # print sigma
    F = ((1 - sigma['sigma']) * sigma['phi']).sum()
    Best = sigma['phi'].sum()
    if out:
        cutoffLine('-')
        print '   F: %f' % F
        print 'Best: %f' % Best
        print ' F/B: %f' % (F/Best*100)

    return F/Best*100
