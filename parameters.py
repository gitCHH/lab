# encoding=utf-8

def dump_seq(m5out_dir):
    '''
    读取dump顺序，直到包含cpu dump1和cpu dump2为止。
    :param m5out_dir:stats.txt所在路径。
    :return:
    '''
    cd1 = False
    cd2 = False
    seq = []
    for line in open(m5out_dir + 'system.pc.com_1.terminal'):
        if cd1 and cd2:
            return seq
        elif line.find('cd1') == 0:
            cd1 = True
            seq.append('cd1')
        elif line.find('cd2') == 0:
            cd2 = True
            seq.append('cd2')
        elif line.find('gd1') == 0:
            seq.append('gd1')
        elif line.find('gd2') == 0:
            seq.append('gd2')


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
    committedOps = []
    conditional_control_insts = []
    Branches = []
    MemRead = []
    MemWrite = []
    No_OpClass = []
    IntAlu = []
    IntMult = []
    IntDiv = []
    FloatAdd = []
    FloatCmp = []
    FloatCvt = []
    FloatMult = []
    FloatDiv = []
    FloatSqrt = []
    n_begin = 0
    demand_hits = []
    GPU_demand_hits = []  # fermi has
    CPU_demand_hits = []  # fermi has
    demand_accesses = []  # misses = accesses -hits
    seq = dump_seq(m5out_dir)
    # print(seq)
    start = seq.index('cd1') + 1
    end = seq.index('cd2') + 1
    # print(start,end)
    for line in open(m5out_dir + 'stats.txt'):
        if line.find('---------- Begin Sim') == 0:
            n_begin = n_begin + 1
        if n_begin > end:
            break
        elif n_begin == start or n_begin == end:
            if line.find('system.cpu') == 0:
                key=line.split()[0]
                # print(key)
                value = int(float(line.split()[1]))  # python3 中取消了long
                # print(key.rfind('committedOps'))
                if key.rfind('committedOps') >= 0:
                    committedOps.append(value)
                elif key.rfind('conditional_control_insts') >= 0:
                    conditional_control_insts.append(value)
                elif key.rfind('Branches') >= 0:
                    Branches.append(value)
                elif key.rfind('op_class::No_OpClass') >= 0:
                    No_OpClass.append(value)
                elif key.rfind('op_class::IntAlu') >= 0:
                    IntAlu.append(value)
                elif key.rfind('op_class::IntMult') >= 0:
                    IntMult.append(value)
                elif key.rfind('op_class::IntDiv') >= 0:
                    IntDiv.append(value)
                elif key.rfind('op_class::FloatAdd')>=0:
                    FloatAdd.append(value)
                elif key.rfind('op_class::FloatCmp') >= 0:
                    FloatCmp.append(value)
                elif key.rfind('op_class::FloatCvt') >= 0:
                    FloatCvt.append(value)
                elif key.rfind('op_class::FloatMult') >= 0:
                    FloatMult.append(value)
                elif key.rfind('op_class::FloatDiv') >= 0:
                    FloatDiv.append(value)
                elif key.rfind('op_class::FloatSqrt') >= 0:
                    FloatSqrt.append(value)
                elif key.rfind('op_class::MemRead') >= 0:
                    MemRead.append(value)
                elif key.rfind('op_class::MemWrite') >= 0:
                    MemWrite.append(value)
            elif line.find('system.ruby.l2_cntrl0.L2cache.demand_hits')==0:
                demand_hits.append(int(line.split()[1]))
            elif line.find('system.ruby.l2_cntrl0.L2cache.GPU_demand_hits') == 0:
                GPU_demand_hits.append(int(line.split()[1]))
            elif line.find('system.ruby.l2_cntrl0.L2cache.CPU_demand_hits') == 0:
                CPU_demand_hits.append(int(line.split()[1]))
            elif line.find('system.ruby.l2_cntrl0.L2cache.demand_accesses') == 0:
                demand_accesses.append(int(line.split()[1]))
    print('general: ', len(committedOps), len(conditional_control_insts), len(Branches), len(No_OpClass))
    print('Int: ', len(IntAlu), len(IntMult), len(IntDiv))
    print('Float: ', len(FloatAdd), len(FloatCmp), len(FloatCvt), len(FloatMult), len(FloatDiv), len(FloatSqrt))
    print('Mem: ', len(MemRead), len(MemWrite))
    print('L2cache: ', len(demand_hits), len(demand_accesses), len(CPU_demand_hits), len(GPU_demand_hits))


readStats('bs', '3_300', 10, 'fermi')
