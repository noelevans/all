"""
    To be used with ipython when it starts up. Create a sym-link to this file in
    the default ipython profile like so:
        ln -s ~/repo/playground/start_ipython.py
                ~/.ipython/profile_default/startup/start_ipython.py
"""

import datetime
import decimal
import itertools
import math
import operator
import random
import re
import timeit

# import matplotlib.pyplot as plt    # very slow
import numpy as np
import pandas as pd
import scipy as sp

from collections import Counter
from pprint import pprint as pp
from sklearn import datasets


pd.set_option('display.max_columns', 30)
pd.set_option('display.width', 100)

df_small = pd.DataFrame([[1,2,3], [2,4,8]], columns=['a', 'b', 'c'])

