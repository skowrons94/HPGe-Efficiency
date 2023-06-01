import numpy as np

from numpy import exp

class Efficiency( ):
    def __init__( self, params ):
        self.params = params

    def effPeak( self, energy ):
        return exp( self.params['a'] + self.params['b']*np.log( energy ) + self.params['c']*pow( np.log( energy ), 2 ) )

    def effTot( self, energy ):
        return self.effPeak( energy )/exp( self.params['k1'] + self.params['k2']*np.log( energy ) + self.params['k3']*pow( np.log( energy ), 2 ) )
