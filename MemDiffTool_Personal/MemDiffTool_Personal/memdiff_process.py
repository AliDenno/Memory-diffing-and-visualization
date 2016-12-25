import memory_dump as md
import configuration as co
import pandas
from bisect import *
from pandas import DataFrame
import time
import os

start_time = time.time()
######## Initialize the Dump file
dump1 = md.MemoryDump(co.dump_memory_location)

######## Cash the processes of the Dump file
# dump1.vol_pslist() #Uncomment for New Dumps
dump1.cashing_of_processes()

######## Cash the modules of each process
# dump1.vol_dlllist() #Uncomment for New Dumps
dump1.cashing_of_modules()

######## Cash the pages of each module
#dump1.vol_memmap() #Uncomment for New Dumps
dump1.cashing_of_pages()


print("--- %s seconds ---" % (time.time() - start_time))










'''
for i in dump1.processes:
    print("{0}::{1}".format(i.pid,len(i.modules)))
'''