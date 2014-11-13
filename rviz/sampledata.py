'''
provide sample dataset from R, return as csv str
'''

from rpy2 import robjects
from rpy2.robjects import Formula, Environment
from rpy2.robjects.vectors import IntVector, FloatVector
from rpy2.robjects.lib import grid
from rpy2.robjects.packages import importr, data

SEPERATOR =","

datasets = importr('datasets')
dataset_names = ["mtcars","CO2","airquality","faithful"]

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class SampleData(object):
  
  _data = {}

  def __init__(self):

    for name in dataset_names:
      onedataset = data(datasets).fetch(name)[name]
      self._data[name] = onedataset

  
  '''
  Return the avalaible dataset list
  '''
  def getlist(self):
    return [i for i in self._data.keys()]

  '''
  Return the CSV data as string of the datasets
  '''
  def getdata(self, dataname):
    result = ""
    data = self._data[dataname]

    if data is not None:
      names = data.rownames
      counter = 0
      header_appended = False
      for row in data.iter_row():
        rowheader = "" + SEPERATOR + SEPERATOR.join(row.names)
        rowvalue = names[counter] + SEPERATOR + SEPERATOR.join([str(i[0]) for i in row])
        counter = counter + 1
        if not header_appended:
          result = result + rowheader
          result = result + '\n'
          header_appended = True

        result = result + rowvalue
        result = result + '\n'
    return result

