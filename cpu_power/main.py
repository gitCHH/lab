#!/usr/bin/python

from multicore import *
'''
import csv
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
'''
import shutil
gen_mcpat_xml_file = True
bench='cedd'
ratios=[]
work_dir=''

def cpu2006_multicore(bench, l2_size, l2_assoc):
    experiment = MulticoreExperiment(ExperimentType.FOUR_PHASE_FS_SIMULATION, work_dir, bench, l2_size, l2_assoc,  0, gen_mcpat_xml_file, True)
    return experiment

def generate_cpu2006_experiments_results():
    def generate_csv_multicore_experiments(benches):
        experiment_l2_sizes = []
        experiment_l2_sizes.append(cpu2006_multicore(bench,'256kB', 8))
    generate_csv_multicore_experiments(bench)


if __name__ == '__main__':
    work_dir='/home/huan/6t/cedd/maxwell_m5out/'
    generate_cpu2006_experiments_results()
    #os.rename(work_dir + '/mcpat_out.txt', work_dir + '/mcpat_out_of_first_section.txt')
    #shutil.copyfile(work_dir +'/stats.txt',work_dir +'/stats_origin.txt')
