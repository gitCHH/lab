# encoding=utf-8

import numpy as np
import matplotlib.pyplot as plt
from cedd_statistics import get_PU_runtime as getCeddRuntime
from statistics import get_PU_runtime as getRuntime
from cedd_tune import predict as predictCedd
from tune import predict

patterns = ["/", "\\", "|", "-", "+", "x", "o", "O", ".", "*"]
hatch = patterns[0]


def f(gpu_arch='fermi', grain=5):
    m5out_dir_home = 'D:/6TTiming/'
    bench_initRatio = {'bs': 10, 'cedd': 20,'rscd': 20}
    GPU_heights = []
    Init_heights = []
    Tuned_heights = []
    for bench in bench_initRatio.keys():
        m5out_dir = m5out_dir_home + bench + '/' + gpu_arch + '_m5out/' + bench + str(
            bench_initRatio[bench]) + '/'
        if bench == 'cedd':
            time_all_GPU = getCeddRuntime(m5out_dir_home + bench + '/' + gpu_arch + '_m5out/' + bench + '0/')
            init_CG_time = getCeddRuntime(m5out_dir)
            new_ratio = predictCedd(init_CG_time[0], bench_initRatio[bench], init_CG_time[1], grain)
            m5out_dir = m5out_dir_home + bench + '/' + gpu_arch + '_m5out/' + bench + str(
                int(new_ratio)) + '/'
            CG_time = getCeddRuntime(m5out_dir)
        else:
            time_all_GPU = getRuntime(m5out_dir_home + bench + '/' + gpu_arch + '_m5out/' + bench + '0/')
            init_CG_time = getRuntime(m5out_dir)
            new_ratio = predict(init_CG_time[0], bench_initRatio[bench], init_CG_time[1], grain)
            m5out_dir = m5out_dir_home + bench + '/' + gpu_arch + '_m5out/' + bench + str(
                int(new_ratio)) + '/'
            CG_time = getRuntime(m5out_dir)
        print('Fermi r:',new_ratio)
        GPU_heights.append(max(time_all_GPU))
        Init_heights.append(max(init_CG_time))
        Tuned_heights.append(max(CG_time))
    print('Fermi GPU',GPU_heights)
    print('Init',Init_heights)
    print('Tuned',Tuned_heights)

    fig, axs = plt.subplots(1, 2, figsize=(4, 6), frameon=False)
    ax = axs[0]
    ax.set_xticklabels(bench_initRatio.keys())
    index = np.arange(1, len(bench_initRatio) + 1)
    bar_width = 0.28
    opacity = 0.3
    ax.set_xticks(index)
    ax.set_title('Fermi GPU')
    ax.set_ylabel('Execution Time(ms)')
    ax.set_xlabel('Benchmarks')
    ax.bar(index - bar_width, GPU_heights, bar_width, hatch='.', alpha=opacity, color='black', label='GPU')
    ax.bar(index, Init_heights, bar_width, hatch='//', alpha=opacity, color='black', label='init')
    ax.bar(index + bar_width, Tuned_heights, bar_width, hatch='\\\\', alpha=opacity, color='black', label='tuned')
    ax.legend()

    GPU_heights.clear()
    Init_heights.clear()
    Tuned_heights.clear()
    gpu_arch = 'maxwell'
    for bench in bench_initRatio.keys():
        m5out_dir = m5out_dir_home + bench + '/' + gpu_arch + '_m5out/' + bench + str(
            bench_initRatio[bench]) + '/'
        if bench == 'cedd':
            time_all_GPU = getCeddRuntime(m5out_dir_home + bench + '/' + gpu_arch + '_m5out/' + bench + '0/')
            init_CG_time = getCeddRuntime(m5out_dir)
            new_ratio = predictCedd(init_CG_time[0], bench_initRatio[bench], init_CG_time[1], grain)
            m5out_dir = m5out_dir_home + bench + '/' + gpu_arch + '_m5out/' + bench + str(
                int(new_ratio)) + '/'
            CG_time = getCeddRuntime(m5out_dir)
        else:
            time_all_GPU = getRuntime(m5out_dir_home + bench + '/' + gpu_arch + '_m5out/' + bench + '0/')
            init_CG_time = getRuntime(m5out_dir)
            new_ratio = predict(init_CG_time[0], bench_initRatio[bench], init_CG_time[1], grain)
            m5out_dir = m5out_dir_home + bench + '/' + gpu_arch + '_m5out/' + bench + str(
                int(new_ratio)) + '/'
            CG_time = getRuntime(m5out_dir)
        print('Maxwell r:', new_ratio)
        GPU_heights.append(max(time_all_GPU))
        Init_heights.append(max(init_CG_time))
        Tuned_heights.append(max(CG_time))
    print('Maxwell GPU', GPU_heights)
    print('Init', Init_heights)
    print('Tuned', Tuned_heights)
    ax = axs[1]
    ax.set_xticklabels(bench_initRatio.keys())
    index = np.arange(1, len(bench_initRatio) + 1)
    ax.set_xticks(index)
    ax.set_title('Maxwell GPU')
    ax.set_ylabel('Execution Time(ms)')
    ax.set_xlabel('Benchmarks')
    ax.bar(index - bar_width, GPU_heights, bar_width, hatch='.', alpha=opacity, color='black', label='GPU')
    ax.bar(index, Init_heights, bar_width, hatch='//', alpha=opacity, color='black', label='init')
    ax.bar(index + bar_width, Tuned_heights, bar_width, hatch='\\\\', alpha=opacity, color='black', label='tuned')
    ax.legend()
    fig.tight_layout()
    plt.show()


f()
