from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from math import pi
from bokeh.io import output_file, show, vplot
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper
from bokeh.plotting import figure
import xml.etree.ElementTree as ET
import memory_dump as md
import process as pr
import module as mod
import page as pge
import time
import heatmap_processess as phmap
import pandas as pd
import numpy as NP
import bokeh.palettes as bp
import configuration as co
import heatmap_processess as phmap
import heatmap_MemoryDump as memmap
import math
import pandas
import bisect_module as bi
import heatmap_summary as shmap
import toolz as tz

def get_index(list_modules,module):
    """
    Search for an element efficiently within a list 
    """
    for index, item in enumerate(list_modules):
        if item.name == module:
            break
        else:
            index = -1
    return index
def parse(heatmap_dump,filename):
    """
    Read and parse an XML file. Convert it to a dump-file object that has processes, modules and pages.
    """
    #start_time = time.time()
    

    #tree = ET.parse('testxml.xml')
    tree = ET.parse(filename)
    root = tree.getroot()

    #print(root[1][0][1].text)
    #print(root[1][0].attrib['size'])
    #print(len(root[1][0]))

    for i in range(0,len(root)):
        #print("{0}:{1}".format(root[i].attrib['name'],root[i].attrib['pid']))
        process=pr.Process(root[i].attrib['name'],root[i].attrib['pid'],root[i].attrib['uncovered_memory_ratio'],root[i].attrib['memory_used_by_pages'],root[i].attrib['covered_memory_by_modules'])
        #print("add process: "+process.name)
        process.UMR=root[i].attrib['uncovered_memory_ratio']

        heatmap_dump.processes.append(process)
        sum_sizes=0
        for j in range(0,len(root[i])):
            #print("--------{0}:{1}".format(root[i][j].attrib['name'],root[i][j].attrib['base']))
            module=mod.Module(root[i][j].attrib['name'],root[i][j].attrib['base'],root[i][j].attrib['size'])
            sum_sizes=sum_sizes+int(module.size,16)
            heatmap_dump.processes[i].modules.append(module)
            for k in range(0,len(root[i][j])):
                #print("----------------{0}".format(root[i][j][k].text))
                tpage=pge.Page(root[i][j][k].text,root[i][j][k].attrib['Asci'],root[i][j][k].attrib['NAsci'],root[i][j][k].attrib['Num'],root[i][j][k].attrib['Ent'],root[i][j][k].attrib['Size'],root[i][j][k].attrib['Hash'],root[i][j][k].attrib['RelativeOffset'])
                heatmap_dump.processes[i].modules[j].pages.append(tpage)

        heatmap_dump.processes[i].sum_sizes=sum_sizes
    return heatmap_dump
def truncate(f, n):
    """
    Truncates/pads a float f to n decimal places without rounding
    """

    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])     
 
if __name__ == '__main__':
   #print("ENTER")
    #heatmap_dump=prase()

    heatmap_dump=md.MemoryDump("heatmap")

    #filename_1="Complete_XML.xml"
    filename_1=co.memory_tovisualize
    #filename_2="Resources\FullXML.xml"
    #filename_3="testxml_withthread_number_27.xml"
   
    heatmap_dump=parse(heatmap_dump,filename_1)

    list_modules=[]
    
    for pr in heatmap_dump.processes:
        for mod in pr.modules:
            mod.name=mod.name.lower()
           
    #Omit the first one
    for pr in heatmap_dump.processes:
        for mod in range(1,len(pr.modules)):
            list_modules.append(pr.modules[mod])
    
    
    list_modules.sort(key = lambda x: x.base)
    list_modules=list(tz.unique(list_modules, key=lambda x: x.name))
    #print(len(list_modules))
    #print("PAUSE")
    #time.sleep(5)
        #print(heatmap_dump.processes[1].summodules)
    #ListOfPages= [[] for i in range(len(list_modules))]
    ListOfobsoletePages= [[] for i in range(len(list_modules))]
    #L=[[],[],[]]

    for pr in heatmap_dump.processes:
        pr.summodules=[0]*len(list_modules)
        #print(len(list_modules))
      
        for mod in pr.modules:
           #print(mod.name)
           index=get_index(list_modules,mod.name)
           if(index!=-1):
  
               #print("module: "+mod.name+" has " +str(len(mod.pages)) +" pages and size of " + str(int(mod.size,0)))
               #time.sleep(5)
               # How many pages percent %
               pr.summodules[index]= sum(int(c.size,0) for c in mod.pages)/int(mod.size,0) 
               #ListOfPages[index].extend(mod.pages)
               ListOfobsoletePages[index].extend(mod.pages)
               #print(str(pr.summodules[index])+" len: "+str(len(str(pr.summodules[index]))) )
               if(len(str(pr.summodules[index]))>4):
                   pr.summodules[index]=float(str(pr.summodules[index])[:6])*100

    #for i in range(0,len(ListOfPages)):
    #    ListOfPages[i]=list(tz.unique(ListOfPages[i], key=lambda x: x.address))
    for i in range(0,len(ListOfobsoletePages)):
        ListOfobsoletePages[i]=list(tz.unique(ListOfobsoletePages[i], key=lambda x: x.rlOffset))

    #op=next((x for x in list_modules if x.name == "ksuser.dll"), None)
    #print(op.name)
    #print (ListOfobsoletePages[20])

    #for i in list_modules:
    #    print(i.name)

    #print(list_modules[49].name)

    SummaryList=[0]*len(list_modules)
    for i in range(0,len(list_modules)):
        if(len(ListOfobsoletePages[i])!=0):
            #print(i)
            xval= (((max(int(node.rlOffset,0) for node in ListOfobsoletePages[i]))/4096)+1)
            yval=(len(ListOfobsoletePages[i]))
            #print("index"+str(indexa))
            #print(int(yval*100/xval))
            #print(int(yval*100/xval))
            SummaryList[i]=int(yval*100/xval)
    
   

    print(SummaryList[20])
    print(list_modules[20].name)
    #print("PAUSING")
    #time.sleep(5)
    '''
    for pr in heatmap_dump.processes:
        for mod in pr.modules:
            index=get_index(list_modules,mod.name)
            flag="NO"
            if(index!=-1):
                if(int(mod.size,0)>=len(ListOfPages[index])*4096):
                    flag="YES"
                else:
                    print(mod.name+"-"+str(int(mod.size,0))+" - "+str(len(ListOfPages[index])*4096)+" "+flag+" "+str(index))
    '''
    memmap.display_summaryheatmap(heatmap_dump,list_modules,SummaryList)

 


        # THIS IS THE FIRST WAY TO DO IT, REMEMBER BY DECLARING EVERY MODULE FOR EVERY PROCESS 
    '''
    for pr in heatmap_dump.processes:
        pr.summodules=[0]*len(list_modules)
        #print(len(list_modules))
        counter=0
        for mod in pr.modules:
           #print(mod.name)
           index=get_index(list_modules,mod.name)
           if(index!=-1):
               counter=counter+1
               pr.summodules[index]=1
        #print(pr.summodules)
        pr.summodules=[x * ((counter/len(list_modules))*1000) for x in pr.summodules]
        #print(pr.summodules)
        #time.sleep(5)
    '''
    # This is the process to be sure of the summary list 
    '''
    print(list_modules[64].name)
    for item in ListOfobsoletePages[64]:
        print(item.rlOffset)
    print((max(int(node.rlOffset,0) for node in ListOfobsoletePages[64])))
    print(hex((max(int(node.rlOffset,0) for node in ListOfobsoletePages[64]))))
    xval= (((max(int(node.rlOffset,0) for node in ListOfobsoletePages[64]))/4096)+1)
    yval=(len(ListOfobsoletePages[64]))
    print("MAXVAL: "+str(xval))
    print("PAGESNUM: "+str(yval))
    #print(xval,yval)
    print(int(yval*100/xval))
    #ksuser.dll
    '''