from math import pi
from bokeh.io import output_file, show, vplot
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper
from bokeh.plotting import figure
import pandas as pd
import numpy as NP
import bokeh.palettes as bp
import configuration as co
import time
import memory_dump as md
import page as pg

def display_summarystarter(dumpM):
    """
    Build and show the content heatmap memory starter
    """
    #print("RIGHT DIRRECT")
    #time.sleep(5)
    # define processes on Y-Axis
    processes=[o.name+" / "+o.pid for o in dumpM.processes]
    # define modules on X-Axis
    Steps=["Starter"]
    #listP=[]*len(listM)
    #Summary_List=[0]*len(listM)
    module = []
    process=[]
    module_index=0
    step=[]
    process_val=[]
    UMR=[]
    for proc in dumpM.processes: # Names of processes
        process.append(proc.name+" / "+proc.pid)
        module.append(1)
        step.append("Starter")
        UMRS=str(proc.UMR)
        if(len(UMRS)>6):
            UMR.append(UMRS[0:6])
        else:
            UMR.append(UMRS)
        #if(len(proc.modules)!=0):
            
            #print(len(proc.modules[0].name))
        process_val.append(proc.name)
        #else:
            #process_val.append("n\a")
    
   
    source = ColumnDataSource(data=dict(module=module, process=process,step=step,process_val=process_val,UMR=UMR))
    TOOLS = "hover,save,pan,box_zoom,wheel_zoom"
    # the figure and its properties 
    p = figure(title="",
               x_range=Steps, y_range=list(reversed(processes)),
               #x_axis_location="above", plot_width=1450, plot_height=700,
               x_axis_location="above", plot_width=50, plot_height=650,
               tools=TOOLS,toolbar_location="above")
    p.border_fill_color = "whitesmoke"
    #p.min_border_bottom = 10
    #p.min_border_right = 10
    p.min_border_left = 40
    p.toolbar.logo = None
    #p.logo=None
    p.toolbar_location = None

    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "1pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = pi / 3
       
    #colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
    colors = ["#f2f2f2", "#990000","#e59400","#e5e500","#007300","#0000e5"]
    
    mapper = LinearColorMapper(palette=colors)

    # modifying every rectangle
    p.rect(x="step", y="process", width=1, height=1,
           source=source,
           # fill_color={'field': 'value', 'transform': mapper},
           fill_color={'field': 'module', 'transform': mapper},
           line_color='white')

    # info to display on hover
    p.select_one(HoverTool).tooltips = [
        ('', '@process_val'),
        ('', '@UMR'),
 
    ]
    p.xaxis.visible = False
    p.yaxis.visible = False

    return(p)