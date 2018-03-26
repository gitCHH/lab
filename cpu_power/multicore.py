#
# A Python script to generate multicore experiment result CSV files from the specified GEM5 config and stat files.
#
# Copyright (C) Min Cai 2015
#

from mcpat import *


class MulticoreExperiment(McPATEnabledExperiment):
   
    @classmethod
    def dump_head_row(cls):
        return [
            'bench',





            'system_runtime_dynamic_power',



            'l2_runtime_dynamic_power',




        ]

    def dump_row(self, baseline_experiment):
        return [
            self.bench,



            




            self.system_runtime_dynamic_power(),



            self.l2_runtime_dynamic_power(),


        ]
