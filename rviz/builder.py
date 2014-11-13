import rpybuilder

class Builder(object):

  def __init__(self, spec):
    ## may use different builder in thr future
    self.builder = rpybuilder.Rpy2Builder(spec)

  def build(self):
    return self.builder.build()