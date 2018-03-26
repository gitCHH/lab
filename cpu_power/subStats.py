# encoding=utf-8
import os

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

'''
Peak Dynamic Power = 6.25626 W
Subthreshold Leakage Power = 13.598 W
Gate Leakage Power = 1.10477 W
Runtime Dynamic Power = 1.52282 W
Runtime Dynamic Energy = 17.9296 J
Total Runtime Energy = 191.04 J
'''
def last_Paragraph(work_dir):
    stats_file =work_dir+'/stats.txt'
    stats_last=work_dir+'/stats_last.txt'
    writer=open(stats_last,'w')
    row=0
    for line in open(stats_file):
        if row >= 22:
            writer.write(line)
        elif line.find('---------- B') >=0:
            row=row+1
            if row>=22:
                writer.write(line)
    writer.flush()
    writer.close()
    os.rename(stats_file,work_dir+'/stats_full.txt')
    os.rename(stats_last,stats_file)
