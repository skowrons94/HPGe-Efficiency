import math
import itertools

import numpy as np

from Efficiency import Efficiency

from uncertainties import ufloat

class YieldBuilder( ):
    def __init__( self, decay_scheme, params, data ):
        self.data = data
        self.decay_scheme = decay_scheme
        self.idx = None
        self.Yield = None
        self.br = 0
        self.eff = Efficiency( params )
        self.run( )

    def run( self ):
        self.Yields, self.Yields_RAW = [ ], [ ]
        for i in range( len( self.decay_scheme.paths ) ):
            self.get_index( i )
            self.calculate_yield( i )
            self.calculate_sum_out( )
            self.calculate_sum_in( )
            sumIn = 0
            for path in self.sumIn:
                sumIn += np.prod( path )
            self.Yields_RAW.append( self.Yield )
            self.Yield *= ( 1 - sum( self.sumOut ) )
            self.Yield += sumIn
            self.Yields.append( self.Yield )

    def calculate_sum_in( self ):
        self.sumIn = [ ]
        orig_lvl = self.decay_scheme.decay.orig_level
        dest_lvl = self.decay_scheme.decay.dest_level
        for decay in orig_lvl.decays:
            if( decay.energy.val == self.decay_scheme.decay.energy.val ):
                continue
            temp = [ ]            
            brNorm = self.get_branching_norm( decay )
            if not math.isnan( decay.rel_intensity.val ):
                br = decay.rel_intensity.val/brNorm
            else:
                br = 1           
            eff    = self.eff.effPeak( decay.energy.val/1000 )
            temp.append( br*eff )
            lvl = decay.dest_level            
            for decay in lvl.decays:
                if( decay.dest_level.energy.val == dest_lvl.energy.val ):
                    brNorm = self.get_branching_norm( decay )
                    if not math.isnan( decay.rel_intensity.val ):
                        br = decay.rel_intensity.val/brNorm
                    else:
                        br = 1            
                    eff = self.eff.effPeak( decay.energy.val/1000 )
                    temp.append( br*eff )
                    self.sumIn.append( temp )

    def calculate_sum_out( self ):
        self.sumOut = [ ]
        for L in range( 0, len( self.effTot ) + 1 ):
            for subset in itertools.combinations( self.effTot, L ):
                if( subset ):
                    self.sumOut.append( np.prod(subset) )

    def check_branching( self, i ):
        brTotal = 1
        for decay in self.decay_scheme.paths[i]:
            brNorm = self.get_branching_norm( decay )           
            if not math.isnan( decay.rel_intensity.val ):
                brTotal *= decay.rel_intensity.val/brNorm
            else:
                branching *= 1
        if( brTotal < 0.01 ):
            return False
        else:
            return True
            
    def calculate_yield( self, i ):
        self.Yield = ufloat( 1, 0 )
        self.effTot = [ ]

        temp = 0
        self.br = 1

        if( not self.check_branching( i ) ):
            self.Yield = ufloat( 0, 0 )
            return

        for decay in self.decay_scheme.paths[i]:
                
            brNorm = self.get_branching_norm( decay )
                
            if not math.isnan( decay.rel_intensity.val ):
                if not math.isnan( decay.rel_intensity.pm ):
                    branching = ufloat( decay.rel_intensity.val, decay.rel_intensity.pm )/brNorm
                else:
                    branching = ufloat( decay.rel_intensity.val, 0 )/brNorm

            else:
                self.Yield = ufloat( 0, 0 )
                return
                
            if( temp < self.idx ):
                self.Yield *= branching
                self.br    *= branching
                eff = self.eff.effTot( decay.energy.val/1000 )
                self.effTot.append( eff )

            elif( temp == self.idx ):
                self.Yield *= branching
                self.br    *= branching
                self.Yield *= self.eff.effPeak( decay.energy.val/1000 )
                    
            elif( temp == self.idx + 1 ):
                self.Yield *= branching
                self.br    *= branching
                eff = self.eff.effTot( decay.energy.val/1000 )
                self.effTot.append( eff )
                
            else:
                eff = self.eff.effTot( decay.energy.val/1000 )
                self.effTot.append( eff*branching )

            temp += 1

    def get_branching_norm( self, decay ):
        norm = 0
        for decay in decay.orig_level.decays:
            if not math.isnan( decay.rel_intensity.val ):
                norm += decay.rel_intensity.val
        return norm

    def get_index( self, i ):
        temp = 0
        for decay in self.decay_scheme.paths[i]:
            if( abs( self.decay_scheme.energy - decay.energy.val ) < 1 ):
                self.idx = temp
                self.energy = self.decay_scheme.energy
            temp += 1