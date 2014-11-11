import rpybuilder

class Builder(object):

  def __init__(self, data, spec):
    self.builder = rpybuilder.Rpy2Builder(data, spec)

  def build(self):
    return self.builder.build()