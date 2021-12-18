import numpy as np
import math

MATURITY = 'five_year'


def div_term(length, term_num=4):
    max_num = length
    term_idx_arr = [int((i*max_num)/term_num) for i in range(term_num+1)]
    i = 0
    div_term_list = []
    while(i<term_num):
        scope = range(term_idx_arr[i], term_idx_arr[i+1])
        div_term_list.append(scope)
        i += 1
    return div_term_list


def snd_vol(obj, colname=MATURITY):
    yield_list = filt_by_col_to_flt(obj, colname)
    n = len(yield_list)
    i=1
    dy_arr = []
    while(i<n):
        dy = np.log(yield_list[i]/yield_list[i-1])
        dy_arr.append(dy)
        i += 1
    avg_dy = sum(dy_arr)/n
    dvy_arr = list(map(lambda x: (avg_dy-x)**2, dy_arr))
    return math.sqrt((sum(dvy_arr)/len(dvy_arr))*252)


def snd_avg_dff(obj, colname=MATURITY):
    yield_list = filt_by_col_to_flt(obj, colname)
    i=1
    dy_arr = []
    while(i<len(yield_list)):
        dy = np.log(yield_list[i]/yield_list[i-1])
        dy_arr.append(dy)
        i += 1
    return sum(dy_arr)/len(dy_arr)


def snd_avg_yld(obj, colname=MATURITY):
    yield_list = filt_by_col_to_flt(obj, colname)
    return sum(yield_list)/len(yield_list)


def snd_std_yld(obj, colname=MATURITY):
    yield_list = filt_by_col_to_flt(obj, colname)
    return stdiv(yield_list)


def snd_avg_std_dff(obj, colname=MATURITY):
    yield_list = filt_by_col_to_flt(obj, colname=colname)
    i=1
    dy_arr = []
    while(i<len(yield_list)):
        dy = np.log(yield_list[i]/yield_list[i-1])
        dy_arr.append(dy)
        i += 1
    return stdiv(dy_arr)


def stdiv(l_data):
    sum_data = sum(l_data)
    n = len(l_data)
    avg_dt = sum_data/n
    sum_dev = 0
    for d in l_data:
        sum_dev += (d-avg_dt)**2
    return sum_dev/n


def filt_by_col_to_flt(obj, colname):
    li = []
    for o in obj:
        val = eval(f'o.{colname}')
        li.append(float(val))
    return li
