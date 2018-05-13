# encoding=utf-8

def dump_seq(m5out_dir):
    '''
    读取dump顺序，直到包含cpu dump1和cpu dump2为止。
    :param m5out_dir:stats.txt所在路径。
    :return:
    '''
    seq = []
    for line in open(m5out_dir + 'system.pc.com_1.terminal'):
        if line.find('cd1') == 0:
            seq.append('cd1')
        elif line.find('cd2') == 0:
            seq.append('cd2')
        elif line.find('gd1') == 0:
            seq.append('gd1')
        elif line.find('gd2') == 0:
            seq.append('gd2')
    return seq


def readStats(bench, workload, f, gpu_arch='maxwell'):
    '''
    分析模拟器中指令数量，第一段为cpu开始计算任务前的stats，第二段为cpu结束计算时的stats，将多个模拟器的多个stats结果存在列表中。
    用dump_seq来指定同一stats文件中的第几段（begin、end simulation之间为一段）。
    :param bench:
    :param workload:
    :param f:
    :param gpu_arch:
    :return:
    '''
    m5out_dir = 'D:/more/' + bench + '_' + workload + '/' + gpu_arch + '_m5out/' + bench + str(f) + '/'
    sim_seconds = []
    demand_hits = []
    GPU_demand_hits = []  # fermi has
    CPU_demand_hits = []  # fermi has
    demand_accesses = []  # misses = accesses -hits
    seq = dump_seq(m5out_dir)
    # print(start,end)
    for line in open(m5out_dir + 'stats.txt'):
        if line.find('sim_seconds') == 0:
            sim_seconds.append(float(line.split()[1]) * 1000)
        elif line.find('system.ruby.l2_cntrl0.L2cache.demand_hits') == 0:
            demand_hits.append(int(line.split()[1]))
        elif line.find('system.ruby.l2_cntrl0.L2cache.GPU_demand_hits') == 0:
            GPU_demand_hits.append(int(line.split()[1]))
        elif line.find('system.ruby.l2_cntrl0.L2cache.CPU_demand_hits') == 0:
            CPU_demand_hits.append(int(line.split()[1]))
        elif line.find('system.ruby.l2_cntrl0.L2cache.demand_accesses') == 0:
            demand_accesses.append(int(line.split()[1]))
    print('---- 数据校验 ----')
    print('len(dumps): ', len(seq))
    print('len(times): ', len(sim_seconds), ',len(L2_hits): ', len(demand_hits))
    cpu_time_dicts = []
    gpu_time_dicts = []
    for i in range(0, len(seq)):
        if seq[i].find('cd') == 0:
            cpu_time_dicts.append({seq[i]: sim_seconds[i]})
        else:
            gpu_time_dicts.append({seq[i]: sim_seconds[i]})
    print('len(cpu_dicts): ', len(cpu_time_dicts))
    print('len(gpu_dicts): ', len(gpu_time_dicts))
    for i in range(0, int(len(gpu_time_dicts) / 2)):
        print(i, ' : ', round(gpu_time_dicts[i * 2 + 1]['gd2'] - gpu_time_dicts[i * 2]['gd1'], 4))
    for j in range(0, int(len(cpu_time_dicts) / 2)):
        print(j, ' : ', round(cpu_time_dicts[j * 2 + 1]['cd2'] - cpu_time_dicts[j * 2]['cd1'], 4))
    for k in range(0, len(seq)):
        if seq[k].find('2') >= 0:
            print(k, 'cpu hitrate: ', round(CPU_demand_hits[k] / demand_accesses[k], 3))
            print(k, 'gpu hitrate: ', round(GPU_demand_hits[k] / demand_accesses[k], 3))
    print('last dump: ', seq[len(seq) - 1], 'last second: ', seq[len(seq) - 2])
    print('interval: ', sim_seconds[len(sim_seconds) - 2] - sim_seconds[len(sim_seconds) - 3])


readStats('cedd', '100', 200, 'fermi')
