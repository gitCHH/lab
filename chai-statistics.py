
n_groups = 5
n_each = 4
n_sections = n_each * n_groups + 1


def check_complete():
    i = 0
    for line in open(m5out_dir + 'system.pc.com_1.terminal', 'r'):
        if line.find('m5 end') >= 0:
            i = i + 1
    print(i)
    if i < n_groups:
        print('warning: groups less than ', n_groups, ', need another ', n_groups - i, ' group(s)')
    i = 0
    for line in open(m5out_dir + 'stats.txt', 'r'):
        if line.find('sim_seconds') >= 0:
            i = i + 1
    print(i)
    if i < n_sections:
        print('warning: sections less than ', n_sections, ',  need another ', n_sections - i, ' section(s)')


def get_runtime():
    i = 0
    runtimes = []
    for line in open(m5out_dir + 'stats.txt', 'r'):
        if line.find('sim_seconds') >= 0:
            i = i + 1
            if i == 1:
                base_runtime = line.split()[1]
            elif i == n_sections - 1:
                finish_runtime = line.split()[1]
                runtimes.append(finish_runtime)
            elif n_sections - n_each * 2 <= i <= n_sections - 1:
                runtimes.append(line.split()[1])
            elif i > n_sections:
                print('warning: section number is not correct.')
    print('base time: ', round(float(base_runtime) * 1000, 3), 'ms, finish time: ',
          round(float(finish_runtime) * 1000, 3), 'ms, (finish - base)/n_groups: ',
          round((float(finish_runtime) - float(base_runtime)) / n_groups * 1000, 3), 'ms')
    return runtimes


def get_dump_sequence():
    res = []
    for line in open(m5out_dir + 'system.pc.com_1.terminal', 'r'):
        if len(res) < n_each * 2 and line.find('dump') >= 0:
            res.append(line.strip())
    if len(res) < 8:
        print('warning: terminal out is not correct.')
    return res[n_each:]


def get_PU_runtime():
    PU_times = get_runtime()
    print('8 runtimes: ', PU_times)
    seq = get_dump_sequence()
    print('dump sequence: ', seq)
    idx_cpu_dump1 = seq.index('cpu dump1')
    idx_cpu_dump2 = seq.index('cpu dump2')
    idx_gpu_dump1 = seq.index('gpu dump1')
    idx_gpu_dump2 = seq.index('gpu dump2')
    if idx_cpu_dump1 < idx_gpu_dump1:
        print('cpu begins before gpu')
    else:
        print('gpu begins before cpu')
    if idx_cpu_dump2 < idx_gpu_dump2:
        print('cpu completes before gpu')
    else:
        print('gpu completes before cpu')

    gpu_runtime = (float(PU_times[idx_gpu_dump2]) - float(PU_times[idx_gpu_dump1]) + float(
        PU_times[idx_gpu_dump2 + n_each]) - float(PU_times[idx_gpu_dump1 + n_each])) / 2 * 1000
    cpu_runtime = (float(PU_times[idx_cpu_dump2]) - float(PU_times[idx_cpu_dump1]) + float(
        PU_times[idx_cpu_dump2 + n_each]) - float(PU_times[idx_cpu_dump1 + n_each])) / 2 * 1000
    print('gpu runtime: ', round(gpu_runtime, 3), 'ms')
    print('cpu runtime: ', round(cpu_runtime, 3), 'ms')
    iteration_time = (float(PU_times[n_each - 1]) - float(PU_times[0]) + float(PU_times[n_each * 2 - 1]) - float(
        PU_times[n_each])) / 2 * 1000
    print('time of each iteration: ', round(iteration_time, 3), 'ms')

# HSTO 0 need rerun, BS need run
benchmark = 'SC'
ratios = ['0','2', '4', '6', '8', '10', '12', '14', '16', '18', '20']
for percent in ratios:
    m5out_dir = 'D:/m5out2t_on_8core/'
    m5out_dir = m5out_dir + benchmark + percent + '/'
    print('----------------benchmark: ', benchmark, ', percent: ', percent, '%-----------------------')
    check_complete()
    # get_PU_runtime()
