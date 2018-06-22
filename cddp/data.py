import numpy as np
import abc


class XCostData(object):
  """ Data structure for state-dependent cost functions
  """
  __metaclass__ = abc.ABCMeta

  def __init__(self, n):
    # State dimension
    self.n = n

    # Creating the data structure of state cost function
    # and its derivatives
    self.l = np.matrix(np.zeros(1))
    self.lx = np.matrix(np.zeros((self.n, 1)))
    self.lxx = np.matrix(np.zeros((self.n, self.n)))


class XUCostData(object):
  """ Data structure for state/control-dependent cost functions
  """
  __metaclass__ = abc.ABCMeta

  def __init__(self, n, m):
    # State and control dimension
    self.n = n
    self.m = m

    # Creating the data structure of state-control cost function and its
    # derivatives
    self.l = np.matrix(np.zeros(1))
    self.lx = np.matrix(np.zeros((self.n, 1)))
    self.lu = np.matrix(np.zeros((self.m, 1)))
    self.lxx = np.matrix(np.zeros((self.n, self.n)))
    self.luu = np.matrix(np.zeros((self.m, self.m)))
    self.lux = np.matrix(np.zeros((self.m, self.n)))


class TerminalCostData(XCostData):
  """ Data structure for terminal costs with a linear residual function.

  The residual is n-dimensional because it depends linearly on the state.
  """
  __metaclass__ = abc.ABCMeta

  def __init__(self, n):
    # Creating the state-related data
    XCostData.__init__(self, n)

    # Creating the state residual and its derivatives
    self.xr = np.matrix(np.zeros((self.n, 1)))


class TerminalResidualCostData(XCostData):
  """ Data structure for terminal costs with a general residual function.

  In general, the residual is k-dimensional, its dimension depends on the
  implementation of this residual.
  """
  __metaclass__ = abc.ABCMeta

  def __init__(self, n, k):
    # Creating the state-related data
    XCostData.__init__(self, n)

    # Residual dimension. Note that the residual is a general function
    # of the state
    self.k = k

    # Creating the data structure of the residual and its derivatives
    self.r = np.matrix(np.zeros((self.k, 1)))
    self.rx = np.matrix(np.zeros((self.k, self.n)))


class RunningCostData(XUCostData):
  """ Data structure for running costs with a linear residual function.

  The residual depends on the state and control. So we split it in the state and
  control residual. The state and control residual have a dimension of n and m,
  respectively.
  """
  __metaclass__ = abc.ABCMeta

  def __init__(self, n, m):
    # Creating the state-control cost data
    XUCostData.__init__(self, n, m)

    # Adding the state and control residual vectors
    self.xr = np.matrix(np.zeros((self.n, 1)))
    self.ur = np.matrix(np.zeros((self.m, 1)))


class RunningResidualCostData(XUCostData):
  """ Data structure for running costs with a general residual function.

  In general, the residual is k-dimensional and depends on the state and control.
  Its dimension is defined in the implementation of it.
  """
  __metaclass__ = abc.ABCMeta

  def __init__(self, n, m, k):
    # Creating the state-control cost data
    XUCostData.__init__(self, n, m)

    # Residual dimension
    self.k = k

    # Adding the residual and its derivatives
    self.r = np.matrix(np.zeros((self.k, 1)))
    self.rx = np.matrix(np.zeros((self.k, self.n)))
    self.ru = np.matrix(np.zeros((self.k, self.m)))


class CostManagerData():
  """ Data structure for the cost manager.

  The cost manager containts the terminal and running costs. Additionally,
  we create a dedicated data structure for the total cost; the sum of cost data.
  The terminal and running costs are stacked in the list.
  """

  def __init__(self):
    self.total = None
    self.terminal = []
    self.running = []


class DynamicsData(object):
  """ Data structure for the system dynamics.

  We only define the Jacobians of the dynamics, and not the Hessians of it, because
  our optimal controller by default uses the Gauss-Newton approximation.
  """
  __metaclass__ = abc.ABCMeta

  def __init__(self, n, m):
    # State and control dimensions
    self.n = n
    self.m = m

    # Creating the data structure for the ODE and its
    # derivative
    self.f = np.matrix(np.zeros((self.n, 1)))
    self.fx = np.matrix(np.zeros((self.n, self.n)))
    self.fu = np.matrix(np.zeros((self.n, self.m)))


class DDPData(object):
  def __init__(self, cost_data, dyn_data):
    self.cost = cost_data
    self.dyn = dyn_data

    # State and control dimensions
    self.n = self.dyn.n
    self.m = self.dyn.m

    # State and control vectors
    self.x = np.matrix(np.zeros((self.n, 1)))
    self.u = np.matrix(np.zeros((self.m, 1)))

    # Feedforward and feedback terms
    self.ufb = np.matrix(np.zeros((self.m, self.n)))
    self.uff = np.matrix(np.zeros((self.m, 1)))

    # Value function and its derivatives
    self.dV = np.matrix(np.zeros(1))
    self.Vx = np.matrix(np.zeros((self.n, 1)))
    self.Vxx = np.matrix(np.zeros((self.n, self.n)))

    # Quadratic approximation of the value function
    self.Qx = np.matrix(np.zeros((self.n, 1)))
    self.Qu = np.matrix(np.zeros((self.m, 1)))
    self.Qxx = np.matrix(np.zeros((self.n, self.n)))
    self.Qxu = np.matrix(np.zeros((self.n, self.m)))
    self.Quu = np.matrix(np.zeros((self.m, self.m)))

    # start and terminal time on the interval
    # self.t0 = 0.
    # self.t1 = 0.

    # starting state in the interval
    # self.x0 = np.matrix(np.zeros((self.n, 1)))
    # # final state on the interval
    # self.x1 = np.matrix(np.zeros((self.n, 1)))

    # self.A = np.matrix(np.zeros((self.n,self.n)))
    # self.b = np.matrix(np.zeros((self.n,1)))
    # self.c = float('Inf')
