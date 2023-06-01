import math        

class DFS:
    def __init__( self, start, decays, levels ):
        self.start = start
        self.end = 0
        self.decays = decays
        self.paths = [ ]
        path = [ ]
        for decay in start.decays:
            if decay in decays:
                self.myDFS( decay, path )

    def myDFS( self, start, path ): 
        path = path + [ start ]
        if start.dest_level.energy.val == self.end:
            self.paths.append( path )
        start = start.dest_level
        for decay in start.decays:
            if decay in self.decays:
                self.myDFS( decay, path )

class DecayScheme:
    def __init__( self, energy, populated_state, nuc ):
        self.nuc = nuc
        self.populated_state = populated_state
        self.energy = self.findNearest( energy )
        self.orig_level, self.decay = self.getState( )
        self.dest_levels = [ ]
        self.dest_decays = [ ]
        self.orig_levels = [ ]
        self.orig_decays = [ ]
        self.destDecay( )
        self.origDecay( )
        self.decays = self.dest_decays + self.orig_decays
        self.levels = self.dest_levels + self.orig_levels
        self.getPaths( )

    def findNearest( self, energy ):
        temp = math.inf
        energyTemp = 0
        for level in self.nuc.adopted_levels.levels:
            for decay in level.decays:
                if( abs( float( energy ) - decay.energy.val ) < temp ):
                    temp = abs( float( energy ) - decay.energy.val )
                    energyTemp = decay.energy.val
        if( temp > 50 ):
            print("Decay not found. Please fix the energy!" )
            return 0
        else:
            return energyTemp
                

    def getState( self ):
        isFound = False
        for level in self.nuc.adopted_levels.levels:
            for decay in level.decays:
                if( decay.energy.val == self.energy ):
                    return level, decay
        print("Level not found. Please fix the energy!")
        return 0, 0

    def getDestDecays( self, level ):
        decays = [ ]
        for decay in level.decays:
            self.dest_decays.append( decay )
            decays.append( decay )
        return decays

    def destDecay( self ):
        isEnd = False
        levels = [ ]
        temp = [ ]
        level = self.decay.dest_level
        levels.append( level )
        self.dest_decays.append( self.decay )
        self.dest_levels.append( level )
        while True:
            temp = levels
            for level in levels:
                if( level.energy.val == 0 ):
                    isEnd = True
                else:
                    isEnd = False
                decays = self.getDestDecays( level )
                for decay in decays:
                    temp.append( decay.dest_level )
            levels = temp
            if( isEnd ):
                break

    def getOrigDecays( self, lev ):
        decays = [ ]
        for level in self.nuc.adopted_levels.levels:
            for decay in level.decays:
                if decay.dest_level == lev:
                    if( decay.orig_level.energy.val <= self.populated_state ):
                        self.orig_decays.append( decay )
                        decays.append( decay )
        return decays

    def origDecay( self ):
        isEnd = False
        levels = [ ]
        level = self.decay.orig_level
        self.orig_levels.append( level )
        levels.append( level )
        while True:
            temp = levels
            for level in levels:
                decays = self.getOrigDecays( level )
                if( decays == [] ):
                    isEnd = True
                    continue
                isEnd = False
                for decay in decays:
                    level = decay.orig_level
                    self.orig_levels.append( level )
                    temp.append( level )
            levels = temp
            if( isEnd ):
                break

    def getPaths( self ):
        idx = 0
        temp = 0
        for i in range( len( self.levels ) ):
            if( self.levels[i].energy.val > temp ):
                temp = self.levels[i].energy.val
                idx = i
                
        self.paths = DFS( self.levels[idx], self.decays, self.levels ).paths
