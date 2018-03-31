# encoding=utf-8

'''
Peak Dynamic Power = 6.25626 W
Subthreshold Leakage Power = 13.598 W
Gate Leakage Power = 1.10477 W
Runtime Dynamic Power = 1.52282 W
Runtime Dynamic Energy = 17.9296 J
Total Runtime Energy = 191.04 J
'''

def check_complete(m5out_dir):
    '''
    Get the dump sequence of CPU and GPU from terminal output.
    :param m5out_dir: Terminal output directory.
    :return: Return a list consisting of 'cdx' and 'gdx'
    '''
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

def valid(total,N):
    '''
    To valid the N.
    :param total: The total number of paragraphs.
    :param N: Nth paragraph.
    :return:True, if legal. Otherwise, False.
    '''
    if N>total:
        print 'N can not greater than total number('+total+') of paragraphs.'
        return False
    else:
        return True

def get_Nth_paragraph(paragraph_idx,work_dir,new_name='newFile.txt'):
    '''
    Get a paragraph of stats.txt.
    :param paragraph_idx: The target paragraph index starting with 1.
    :param work_dir: The stats.txt reside.
    :param new_name: The new file name be written into.
    :return: True, if no exception. Otherwise, False. False will be returned if Invalid paragraph index.
    '''
    dump_sequence=check_complete(work_dir)
    total=len(dump_sequence)+1
    #if not valid(total,paragraph_idx):
    #    return False
    stats_file = work_dir + '/stats.txt'
    stats_first = work_dir + new_name
    writer = open(stats_first, 'w')
    target_idx=0
    for line in open(stats_file):
        if line.find('---------- B') >= 0:
            target_idx=target_idx+1
        if target_idx==paragraph_idx:
                writer.write(line)
    writer.flush()
    writer.close()

def common_generator(bench,ratios,cpu_threads='6',gpu_arch='maxwell'):
    for R in ratios:
        work_dir='/home/huan/'+cpu_threads+'t/'+bench+'/'+gpu_arch+'_m5out/'+bench+R+'/'
        dump_sequence=check_complete(work_dir)
        #idx_CGD={}
        for i in range(1,5):
            #idx_CGD[i]=dump_sequence[i]
            new_file='stats_'+str(i)+'_'+dump_sequence[i-1]
            get_Nth_paragraph(i,work_dir,new_file)

def cedd_generator(ratios,cpu_threads,gpu_arch = 'maxwell'):
    bench = 'cedd'
    for R in ratios:
        work_dir = '/home/huan/' + cpu_threads + 't/' + bench + '/' + gpu_arch + '_m5out/' + bench + R + '/'
        dump_sequence = check_complete(work_dir)
        # idx_CGD={}
        idx_cpu_dump1 = dump_sequence.index('cd1')
        idx_cpu_dump2 = len(dump_sequence) - 1 - dump_sequence[::-1].index('cd2')
        idx_gpu_dump1 = dump_sequence.index('gd1')
        idx_gpu_dump2 = len(dump_sequence) - 1 - dump_sequence[::-1].index('gd2')
        get_Nth_paragraph(idx_cpu_dump1+1,work_dir,'stats_'+str(idx_cpu_dump1+1)+'_cd1')
        get_Nth_paragraph(idx_cpu_dump2+1,work_dir,'stats_'+str(idx_cpu_dump2+1)+'_cd2')
        get_Nth_paragraph(idx_gpu_dump1+1,work_dir,'stats_'+str(idx_gpu_dump1+1)+'_gd1')
        get_Nth_paragraph(idx_gpu_dump2+1,work_dir,'stats_'+str(idx_gpu_dump2+1)+'_gd2')

def all_on_GPU_CPU(bench,cpu_threads='6',gpu_arch='maxwell'):
    work_dir = '/home/huan/' + cpu_threads + 't/' + bench + '/' + gpu_arch + '_m5out/' + bench + '0/'
    dump_sequence = check_complete(work_dir)
    get_Nth_paragraph(len(dump_sequence),work_dir,'stats_allGPU.txt')
    #work_dir = '/home/huan/' + cpu_threads + 't/' + bench + '/' + gpu_arch + '_m5out/' + bench + '100/'
    #dump_sequence = check_complete(work_dir)
    #get_Nth_paragraph(len(dump_sequence), work_dir, 'stats_allCPU.txt')

if __name__ == '__main__':
    ratios = ['0', '5', '10', '15', '20', '25', '30', '35']
    pass


