# encoding=utf-8

import numpy as np
import matplotlib.pyplot as plt
# 返回在CPU上处理的数据比例,time(ms),ratio(%)
# crazy idea: GPU处理100%的数据后，预测一个比例，或预测CPU上处理一些数据会性能会更好
def predict(cpu_time, cpu_ratio,gpu_time,grain):
    c_v=cpu_ratio/cpu_time # 整除，两个整数，结果为整数
    g_v=(100-cpu_ratio)/gpu_time
    res=100*c_v/(c_v+g_v)
    if int(res)%grain==0:
        return res
    elif g_v>c_v:
        return int(res)-int(res)%grain
    elif g_v<c_v:
        return int(res)-int(res)%grain+grain # 不知为何返回float， why?

def check_complete(m5out_dir):
    i = False
    j = False
    dump_sequence=[]
    for line in open(m5out_dir + 'system.pc.com_1.terminal', 'r'):
        if i and j:
            break
        if line.find('gd1')==0:
            dump_sequence.append('gd1')
        elif line.find('cd1')==0:
            dump_sequence.append('cd1')
        elif line.find('gd2') == 0:
            i = True
            dump_sequence.append('gd2')
        elif line.find('cd2') == 0:
            j = True
            dump_sequence.append('cd2')
    if i and j:
        return dump_sequence
    else:
        dump_sequence.clear()
        return dump_sequence

def get_runtime(time_count, m5out_dir):
    runtimes = []
    for line in open(m5out_dir + 'stats.txt', 'r'):
        if line.find('sim_seconds') >= 0 and len(runtimes)<time_count:
            runtimes.append(float(line.split()[1]))
    return runtimes
def get_PU_runtime(m5out_dir):
    dump_sequence=check_complete(m5out_dir)
    if len(dump_sequence)<=0:
        print(m5out_dir+'实验结果不完整。')
    else:
        PU_times = get_runtime(len(dump_sequence), m5out_dir)
        idx_gpu_dump1=dump_sequence.index('gd1')
        idx_gpu_dump2=dump_sequence.index('gd2')
        idx_cpu_dump1=dump_sequence.index('cd1')
        idx_cpu_dump2=dump_sequence.index('cd2')
        gpu_runtime = (PU_times[idx_gpu_dump2]-PU_times[idx_gpu_dump1])*1000
        cpu_runtime = (PU_times[idx_cpu_dump2]-PU_times[idx_cpu_dump1])*1000
        time_CG=[]
        time_CG.append(cpu_runtime)
        time_CG.append(gpu_runtime)
        return time_CG

def plot(cpu_init_ratio,bench,n_threads=6,gpu_arch='maxwell',grain=5):
    m5out_dir='/home/huan/'+str(n_threads)+'t/'+bench+'/'+gpu_arch+'_m5out/'+bench+str(cpu_init_ratio)+'/'
    init_CG_time=get_PU_runtime(m5out_dir)
    new_ratio=predict(init_CG_time[0],cpu_init_ratio,init_CG_time[1],grain)
    m5out_dir='/home/huan/'+str(n_threads)+'t/'+bench+'/'+gpu_arch+'_m5out/'+bench+str(int(new_ratio))+'/'
    CG_time=get_PU_runtime(m5out_dir)
    fig, axs = plt.subplots(1, 1, figsize=(4, 6), frameon=False)
    ax = axs
    ratios=[cpu_init_ratio,new_ratio]
    index = np.arange(1, len(ratios) + 1)
    cpu_heights=[init_CG_time[0],CG_time[0]]
    gpu_heights=[init_CG_time[1],CG_time[1]]
    max_heights=[max(init_CG_time),max(CG_time)]
    bar_width = 0.35
    opacity = 0.4
    ax.set_xticklabels(ratios)
    ax.set_xticks(index)
    ax.set_title(bench)
    ax.set_ylabel('Execution Time(ms)')
    ax.set_xlabel('Data Ratio of CPU(%)')
    # ax.set_xlim(0,20)
    # ax.set_ylim(0,10)
    ax.bar(index - bar_width, cpu_heights, bar_width, alpha=opacity, color='r', label='CPU')
    ax.bar(index, gpu_heights, bar_width, alpha=opacity, color='b', label='GPU')
    ax.plot(index, max_heights, color='black', linestyle='--', marker='o', alpha=opacity)
    ax.legend()
    fig.tight_layout()
    plt.show()

#plot(5,'rscd',6,'maxwell',5)
