import math

import numpy as np

from DecayScheme import DecayScheme
from YieldBuilder import YieldBuilder

from uncertainties import ufloat

class Residue( ):
    def __init__( self, data, nuc, states ):
        self.data = data
        self.nuc = nuc
        self.states = states
        self.create_decay_schemes( )

    def get_branching_norm( self, decay ):
        orig_level = decay.orig_level
        norm = 0
        for decay in orig_level.decays:
            if not math.isnan( decay.rel_intensity.val ):
                br = decay.rel_intensity.val
            else:
                br = 0
            norm += br
        return norm

    def dump_decay_scheme( self, decay_scheme, gamma, state ):
        print( gamma, " keV - " + str( len( decay_scheme.paths ) ) + " different paths found for populated state {} with {} branching!\n".format(state[0],state[1]) )
        for path in decay_scheme.paths:
            brTotal = state[1]
            for decay in path:
                brNorm = self.get_branching_norm( decay )            
                if not math.isnan( decay.rel_intensity.val ):
                    branching = decay.rel_intensity.val/brNorm
                else:
                    branching = 1
                brTotal *= branching            
            temp = ""
            for i, gamma in enumerate( path ):
                if( i == len( path ) - 1 ):
                    temp += str( gamma.energy.val ) + " (" + str( gamma.rel_intensity.val ) +  ")"
                else:
                    temp += str( gamma.energy.val ) + " (" + str( gamma.rel_intensity.val ) +  ") -- "
            print( temp + "\tTotal Probability: " + str( brTotal ) )
        print( "\n---------------------------------------------------------------------------------\n" )
            
    def create_decay_schemes( self ):
        self.decay_schemes = { }
        for state in self.states:
            key = str(state[0])
            self.decay_schemes[key] = { }
            for gamma in self.data.values.keys( ):
                self.decay_schemes[key][gamma] = DecayScheme( gamma, state[0], self.nuc )
                self.dump_decay_scheme( self.decay_schemes[key][gamma], gamma, state )

    def set_rate( self, params ):
        self.rate = 1
        for state in self.states:
            if( state[0] == 12541.5 ):
                self.rate = params["R_Al"]
            elif( state[0] == 7556.5 ):
                self.rate = params["R_N"]

    def get_chi2( self, params ):
        residues = [ ]
        self.set_rate( params )
        for gamma in self.data.values.keys( ):
            for i in range( len( self.data.values[gamma].Yield ) ):
                model = 0
                for state in self.states:
                    key = str(state[0])
                    Yield  = YieldBuilder( self.decay_schemes[key][gamma], params, self.data )
                    model += self.rate*state[1]*sum( Yield.Yields )
                data = self.data.values[gamma].Yield[i]                
                error = np.sqrt( pow( self.data.values[gamma].YieldErr[i], 2 ) + pow( model.std_dev, 2 ) )
                residues.append( pow( ( model.nominal_value - data )/error, 2 ) )
        return residues
    
    def get_disc( self, params ):
        disc = [ ]
        self.set_rate( params )
        for gamma in self.data.values.keys( ):
            for i in range( len( self.data.values[gamma].Yield ) ):
                model = 0
                for state in self.states:
                    key = str(state[0])
                    Yield  = YieldBuilder( self.decay_schemes[key][gamma], params, self.data )
                    model += self.rate*state[1]*sum( Yield.Yields )    
                data = ufloat( self.data.values[gamma].Yield[i], self.data.values[gamma].YieldErr[i] )      
                disc.append( ( model - data )/data )
        return disc
    
    def get_yields( self, params ):
        yields = [ ]
        self.set_rate( params )
        for gamma in self.data.values.keys( ):
            for i in range( len( self.data.values[gamma].Yield ) ):
                model = 0
                for state in self.states:
                    key = str(state[0])
                    Yield  = YieldBuilder( self.decay_schemes[key][gamma], params, self.data )
                    model += self.rate*state[1]*sum( Yield.Yields )                
                yields.append( model )
        return yields
    
    def get_yields_no_sum( self, params ):
        yields = [ ]
        self.set_rate( params )
        for gamma in self.data.values.keys( ):
            for i in range( len( self.data.values[gamma].Yield ) ):
                model = 0
                for state in self.states:
                    key = str(state[0])
                    Yield  = YieldBuilder( self.decay_schemes[key][gamma], params, self.data )
                    model += self.rate*state[1]*sum( Yield.Yields_RAW )                
                yields.append( model )
        return yields
    
    def get_data( self ):
        data = [ ]
        for key in self.data.values.keys( ):
            for i in range( len( self.data.values[key].Yield ) ): 
                dat = ufloat( self.data.values[key].Yield[i], self.data.values[key].YieldErr[i] )
                data.append( dat )
        return data
    
    def get_energies( self ):
        energies = [ ]
        for key in self.data.values.keys( ):
            for i in range( len( self.data.values[key].Yield ) ): 
                energies.append( float(key) )
        return energies