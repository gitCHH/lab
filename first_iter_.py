# encoding=utf-8

# 取得第一次运行（iteration）CPU/GPU各自的执行时间的脚本

import numpy as np
import matplotlib.pyplot as plt


# 检查terminal output中是否都存在 gd2/cd2,dump flag数组为空表示实验结果不完整！
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

# 时间个数，m5out_dir
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


ratios = ['0','5', '10', '15', '20', '25', '30', '35']
index=np.arange(1,len(ratios)+1)
bar_width=0.35
opacity = 0.4

def plot(n_thread,bench,gpu_arch='maxwell'):
    fig,axs=plt.subplots(1,1,figsize=(6,9),frameon =False)
    cpu_heights=[]
    gpu_heights=[]
    max_heights=[]# to draw line
    for percent in ratios:
        m5out_dir = '/home/huan/'+str(n_thread)+'t/'+bench+'/'+gpu_arch+'_m5out/'
        m5out_dir = m5out_dir + bench + percent + '/'
        time_CG=get_PU_runtime(m5out_dir)
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
# HSTI, HSTO, SC are not balance
plot(6,'rscd','maxwell')