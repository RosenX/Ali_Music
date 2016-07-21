from utility import *
import csv
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime
import math
import statsmodels.api as sm
from evaluate import evaluate
from pandas import DataFrame
from pandas import Series
from pandas import Timedelta



mpl.style.use('ggplot')

PIC_DIR = 'pic'
DATA_DIR = 'data'
ACTIONS_FILE = 'data/actions.csv'
SONGS_FILE = 'data/songs.csv'
RULE_TRAIN_SET = 'data/rule_train_set.csv'
RULE_TEST_SET = 'data/rule_test_set.csv'
MODEL_TRAIN_SET = 'data/model_train_set.csv'
MODEL_TEST_X_SET = 'data/model_test_x_set.csv'
MODEL_TEST_REAL_SET = 'data/model_test_real_set.csv'
BEHAVIOR_STAT = 'data/behavior_stat.csv'
NEW_ACTIONS_FILE = 'data/new_actions.csv'
