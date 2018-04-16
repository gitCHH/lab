# encoding=utf-8

# 取得cedd在GPU、CPU上的运行时间,这个时间是处理完全部被分配到的frame，并画出条形图

import numpy as np
import matplotlib.pyplot as plt

n_frame = 20

# 检查terminal output中 gd2/cd2数量之和是否等于n_frame,dump flag数组为空表示实验结果不完整！
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

ratios = ['0','5', '10', '15', '20', '25', '30']
index=np.arange(1,len(ratios)+1)
bar_width=0.35
opacity = 0.4

def plot(n_thread,bench,gpu_arch):
    fig,axs=plt.subplots(1,1,figsize=(6,9),frameon =False)
    cpu_heights=[]
    gpu_heights=[]
    max_heights=[]# to draw line
    for percent in ratios:
        m5out_dir = 'D:/6TTiming/'+bench+'/'+gpu_arch+'_m5out/'
        m5out_dir = m5out_dir + bench + percent + '/'
        time_CG=get_PU_runtime(m5out_dir)
        if len(time_CG)<=1:
            break
        cpu_heights.append(time_CG[0])
        gpu_heights.append(time_CG[1])
        max_heights.append(max(time_CG))
    print('cpu: ',cpu_heights)
    print('gpu: ',gpu_heights)
    ax=axs
    ax.set_xticklabels(ratios)
    ax.set_xticks(index)
    ax.set_title(bench)
    ax.set_ylabel('Execution Time(ms)')
    ax.set_xlabel('Data Ratio of CPU(%)')
    #ax.set_xlim(0,20)
    #ax.set_ylim(0,10)
    ax.bar(index-bar_width,cpu_heights,bar_width,alpha=opacity,color='r',label='CPU')
    ax.bar(index,gpu_heights,bar_width,alpha=opacity,color='b',label='GPU')
    ax.plot(index,max_heights,color='black',linestyle='--', marker='o',alpha=opacity)
    ax.legend()

    fig.tight_layout()
    plt.show()

plot(6,'cedd','fermi')