# encoding=utf-8

import numpy as np
import matplotlib.pyplot as plt

n_frame = 20

# 返回在CPU上处理的数据比例,time(ms),ratio(%)
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
    dump_sequence=[]
    for line in open(m5out_dir + 'system.pc.com_1.terminal', 'r'):
        if line.find('gd1')==0:
            dump_sequence.append('gd1')
        elif line.find('cd1')==0:
            dump_sequence.append('cd1')
        elif line.find('gd2') == 0:
            dump_sequence.append('gd2')
        elif line.find('cd2') == 0:
            dump_sequence.append('cd2')
    return dump_sequence

# 时间个数，m5out_dir
def get_runtime(time_count, m5out_dir):
    runtimes = []
    for line in open(m5out_dir + 'stats.txt', 'r'):
        if line.find('sim_seconds') >= 0 and len(runtimes)<time_count:
            runtimes.append(float(line.split()[1]))
    return runtimes


def get_PU_runtime(m5out_dir):
    dump_sequence=check_complete(m5out_dir)
    if len(dump_sequence)!=2*n_frame:
        print(m5out_dir+'实验结果不完整。')
    else:
        PU_times = get_runtime(len(dump_sequence), m5out_dir)
        time_CG = []
        if dump_sequence.count('cd1')<=0 or dump_sequence.count('cd2')<=0:
            time_CG.append(0)
        else:
            idx_cpu_dump1 = dump_sequence.index('cd1')
            idx_cpu_dump2 = len(dump_sequence) - 1 - dump_sequence[::-1].index('cd2')
            cpu_runtime = (PU_times[idx_cpu_dump2] - PU_times[idx_cpu_dump1]) * 1000
            time_CG.append(cpu_runtime)
        # dump1是第一次，dump2是最后一次
        idx_gpu_dump1=dump_sequence.index('gd1')
        idx_gpu_dump2=len(dump_sequence)-1- dump_sequence[::-1].index('gd2')
        gpu_runtime = (PU_times[idx_gpu_dump2]-PU_times[idx_gpu_dump1])*1000
        time_CG.append(gpu_runtime)
        return time_CG

def plot(cpu_init_ratio,bench,n_threads,gpu_arch,grain):
    m5out_dir='D:/6TTiming/'+bench+'/'+gpu_arch+'_m5out/'+bench+str(cpu_init_ratio)+'/'
    init_CG_time=get_PU_runtime(m5out_dir)
    new_ratio=predict(init_CG_time[0],cpu_init_ratio,init_CG_time[1],grain)
    m5out_dir='D:/6TTiming/'+bench+'/'+gpu_arch+'_m5out/'+bench+str(int(new_ratio))+'/'
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

plot(20,'cedd',6,'fermi',5)
