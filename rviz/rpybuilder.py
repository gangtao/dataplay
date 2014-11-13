## This module provide r function through rpy2

import time

import pandas

from rpy2 import robjects
from rpy2.robjects import Formula, Environment
from rpy2.robjects.vectors import IntVector, FloatVector
from rpy2.robjects.lib import grid
from rpy2.robjects.packages import importr, data
import rpy2.robjects.lib.ggplot2 as ggplot2
 
# The R 'print' function
rprint = robjects.globalenv.get("print")
stats = importr('stats')
grdevices = importr('grDevices')
base = importr('base')
datasets = importr('datasets')
mtcars = data(datasets).fetch('mtcars')['mtcars']

class Rpy2Builder(object):

  def __init__(self, spec):
    ## generate png file information
    self.sfilebase = "./static/viz/"
    self.cfilebase = "/viz/"
    self.fileid = str(time.time())
    self.filename = "viz" + self.fileid + ".png"
    self.sfilename = self.sfilebase + self.filename
    self.cfilename = self.cfilebase + self.filename

    ## data set information
    self.spec = spec

  def build(self):
    ##print grdevices.palette()
    if self.spec['type'] == 'csv' :
        df = robjects.DataFrame.from_csvfile('./data/' + self.spec['name'] + '.csv')
    else :
        print type(self.spec['name'])
        samplename = self.spec['name'].encode('ascii','ignore')
        df = data(datasets).fetch(samplename)[samplename]

    #print df
    grdevices.png(file=self.sfilename, width=700, height=400)
    pp = ggplot2.ggplot(df)

    ppargs = {}

    if len(self.spec['viz[xaxis]']) != 0 :
        ppargs['x'] = self.spec['viz[xaxis]']

    if len(self.spec['viz[yaxis]']) != 0 :
        ppargs['y'] = self.spec['viz[yaxis]']

    if len(self.spec['viz[color]']) != 0 :
        ppargs['colour'] = self.spec['viz[color]']

    if len(self.spec['viz[shape]']) != 0 :
        ppargs['shape'] = self.spec['viz[shape]']

    player1 = self.spec['viz[layer1]'] if len(self.spec['viz[layer1]']) != 0 else None
    player2 = self.spec['viz[layer2]'] if len(self.spec['viz[layer2]']) != 0 else None 

    pp = pp + ggplot2.aes_string(**ppargs)
    ##pp = pp + ggplot2.geom_bar(stat="identity", fill="white", colour="darkgreen")
    ##pp = pp + ggplot2.scale_fill_brewer(palette="blues")
    ##pp = pp + ggplot2.geom_point() 
    pp = pp + ggplot2.geom_point(size=5) 
    pp.plot()
    grdevices.dev_off()
    return self.cfilename