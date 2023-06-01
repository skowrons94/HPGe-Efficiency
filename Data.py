import numpy as np

from uncertainties import ufloat

class DataStruct:
    def __init__( self, size ):
        self.Yield = np.zeros( size )
        self.YieldErr = np.zeros( size )

class Data:
    def __init__( self, dataFile ):
        self.dataFile = open( dataFile, "r" )
        self.Lines = self.dataFile.readlines( )
        self.values = { }
        self.read_data( )

    def create_keys( self ):
        keys = [ ]
        for line in self.Lines:
            l = line.split( )
            if( "#" in l[0] ):
                continue
            if( l[0] not in keys ):
                keys.append( l[0] )
        return keys

    def create_data( self ):
        keys = self.create_keys( )
        for key in keys:
            size = 0
            for line in self.Lines:
                l = line.split( )
                if( key == l[0] ):
                    size += 1
            self.values[key] = DataStruct( size )

    def read_data( self ):
        self.create_data( )
        for key in self.values.keys( ):
            i = 0
            for line in self.Lines:
                l = line.split( )
                if( key == l[0] ):
                    self.values[key].Yield[i] = float( l[1] )
                    self.values[key].YieldErr[i] = float( l[2] )

    def dump_data( self ):
        for key in self.values.keys( ):
            for i in range( len( self.values[key].Yield ) ):
                print( self.values[key].Yield[i], "\t", self.values[key].YieldErr[i], "\t", self.values[key].angCorr[i] )
