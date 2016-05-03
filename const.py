import csv
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime
import math
from evaluate import evaluate
from pandas import DataFrame


mpl.style.use('ggplot')

PIC_DIR = 'pic'
DATA_DIR = 'data'
ACTIONS_FILE = 'data/actions.csv'
SONGS_FILE = 'data/songs.csv'
NEW_ACTIONS_FILE = 'data/new_actions.csv'
