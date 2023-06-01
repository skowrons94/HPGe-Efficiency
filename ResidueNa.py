import numpy as np

from Efficiency import Efficiency

from uncertainties import ufloat

class ResidueNa( ):
    def __init__( self, data, nuc, populated_state ):
        self.nuc = nuc
        self.populated_state = populated_state
        self.data = data

    def get_chi2( self, params ):
        residues = [ ]
        eff = Efficiency( params )
        key1, key2 = "511", "1274.57"
        eff_avg = self.data.data[key1].Yield[0]/( ( 1 - eff.effTot( 1.27457 ) )*1.807 )
        eff_tot_avg = eff_avg/( np.exp( params["k1"] + params["k2"]*np.log( 0.511 ) + params["k3"]*pow( np.log( 0.511 ), 2 ) ) )
        Yield = eff.effPeak( float( key2 )/1000 )*( 1 - 1.807*eff_tot_avg )
        residues.append( pow( ( Yield - self.data.data[key2].Yield[0] )/self.data.data[key2].YieldErr[0], 2 ) )
        return residues
    
    def get_disc( self, params ):
        disc = [ ]
        eff = Efficiency( params )
        key1, key2 = "511", "1274.57"
        eff_avg = self.data.data[key1].Yield[0]/( ( 1 - eff.effTot( 1.27457 ) )*1.807 )
        eff_tot_avg = eff_avg/( np.exp( params["k1"] + params["k2"]*np.log( 0.511 ) + params["k3"]*pow( np.log( 0.511 ), 2 ) ) )
        Yield = eff.effPeak( float( key2 )/1000 )*( 1 - 1.807*eff_tot_avg )
        disc.append( ufloat( ( Yield - self.data.data[key2].Yield[0] )/self.data.data[key2].Yield[0], 0 ) )
        return disc
    
    def get_yields( self, params ):
        yields = [ ]
        eff = Efficiency( params )
        key1, key2 = "511", "1274.57"
        eff_avg = self.data.data[key1].Yield[0]/( ( 1 - eff.effTot( 1.27457 ) )*1.807 )
        eff_tot_avg = eff_avg/( np.exp( params["k1"] + params["k2"]*np.log( 0.511 ) + params["k3"]*pow( np.log( 0.511 ), 2 ) ) )
        yields.append( ufloat( eff.effPeak( float( key2 )/1000 )*( 1 - 1.807*eff_tot_avg ), 0 ) )
        return yields
    
    def get_yields_no_sum( self, params ):
        yields = [ ]
        key = "1274.57"
        eff = Efficiency( params )
        yields.append( ufloat( eff.effPeak( float( key )/1000 ), 0 ) )
        return yields
    
    def get_data( self ):
        key = "1274.57"
        data = [ ufloat( self.data.data[key].Yield[0], self.data.data[key].YieldErr[0] ) ]
        return data
    
    def get_energies( self ):
        energies = [ 1274.57 ]
        return energies
