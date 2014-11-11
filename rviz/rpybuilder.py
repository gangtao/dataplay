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

  def __init__(self, data, spec):
    self.sfilebase = "./static/viz/"
    self.cfilebase = "/viz/"
    self.fileid = str(time.time())
    self.filename = "viz" + self.fileid + ".png"
    self.sfilename = self.sfilebase + self.filename
    self.cfilename = self.cfilebase + self.filename

  def build(self):
    ##print grdevices.palette()
    df = robjects.DataFrame.from_csvfile('./data/simple.csv')
    grdevices.png(file=self.sfilename, width=700, height=400)
    pp = ggplot2.ggplot(df)
    pp = pp + ggplot2.aes_string(x='C',y='B',shape='A', colour='A')
    ##pp = pp + ggplot2.geom_bar(stat="identity", fill="white", colour="darkgreen")
    ##pp = pp + ggplot2.scale_fill_brewer(palette="blues")
    ##pp = pp + ggplot2.geom_point() 
    pp = pp + ggplot2.geom_point(size=5) 
    pp.plot()
    grdevices.dev_off()
    return self.cfilename