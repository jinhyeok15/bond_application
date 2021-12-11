import numpy as np
import math

def div_term(obj, term_num=4):
    li_yield = obj_to_yield(obj)
    max_num = len(li_yield)
    term_idx_arr = [int((i*max_num)/term_num) for i in range(term_num+1)]
    i = 0
    div_term_list = []
    while(i<term_num):
        scope = range(term_idx_arr[i], term_idx_arr[i+1])
        div_term_list.append(scope)
        i += 1
    return div_term_list


def snd_vol(obj):
    yield_list = obj_to_yield(obj)
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


def snd_avg_dff(obj):
    yield_list = obj_to_yield(obj)
    i=1
    dy_arr = []
    while(i<len(yield_list)):
        dy = np.log(yield_list[i]/yield_list[i-1])
        dy_arr.append(dy)
        i += 1
    return sum(dy_arr)/len(dy_arr)


def snd_avg_yld(obj):
    yield_list = obj_to_yield(obj)
    return sum(yield_list)/len(yield_list)


def snd_std_yld(obj):
    yield_list = obj_to_yield(obj)
    return stdiv(yield_list)


def snd_avg_std_dff(obj):
    yield_list = obj_to_yield(obj)
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


def obj_to_yield(obj):
    li = []
    for o in obj:
        li.append(float(o.five_year))
    return li
