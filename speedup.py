# encoding=utf-8

import numpy as np
import matplotlib.pyplot as plt
import cedd_statistics
import first_iter_
import cedd_tune
import tune

patterns = [ "/" , "\\" , "|" , "-" , "+" , "x", "o", "O", ".", "*" ]
hatch=patterns[0]

def plot(n_threads=6,gpu_arch='maxwell',grain=5):
    bench_initRatio={'bs':10,'cedd':20,'rscd':20}
    bench='bs'
    m5out_dir = '/home/huan/' + str(n_threads) + 't/' + bench + '/' + gpu_arch + '_m5out/' + bench + str(
        bench_initRatio[bench]) + '/'
    if bench=='cedd':
        time_all_GPU=cedd_statistics.get_PU_runtime('/home/huan/6t/cedd/cedd0/')
        init_CG_time = cedd_statistics.get_PU_runtime(m5out_dir)
        new_ratio = cedd_tune.predict(init_CG_time[0], bench_initRatio[bench], init_CG_time[1], grain)
        m5out_dir = '/home/huan/' + str(n_threads) + 't/' + bench + '/' + gpu_arch + '_m5out/' + bench + str(
        int(new_ratio)) + '/'
        CG_time = cedd_statistics.get_PU_runtime(m5out_dir)
    else:
        init_CG_time = first_iter_.get_PU_runtime(m5out_dir)
        new_ratio = tune.predict(init_CG_time[0], bench_initRatio[bench], init_CG_time[1], grain)
        m5out_dir = '/home/huan/' + str(n_threads) + 't/' + bench + '/' + gpu_arch + '_m5out/' + bench + str(
            int(new_ratio)) + '/'
        CG_time = first_iter_.get_PU_runtime(m5out_dir)
    fig, axs = plt.subplots(1, 1, figsize=(4, 6), frameon=False)
    ax = axs