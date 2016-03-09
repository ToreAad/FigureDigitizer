# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from descartes.patch import PolygonPatch

COLORMAP = "cubehelix_r"

#VRES = 25
#HRES = 100
LINEWIDTH = MARKERSIZE = 10
LINEWIDTH = 2

class Draw(object):
    """
    
    """
    def _MakePlot(self, title):
        """
        
        """
        fig = plt.figure(1, dpi=150)
        ax = fig.add_subplot(111)
        ax.set_title(title)
        
#        ax.set_aspect(125)
        ax.set_xlim(*self.model.xrange)
        
        ax.set_ylim(*self.model.yrange)
        
        return ax
    
    
    def _GetColorbar(self, vmin, vmax, colormap = COLORMAP):
        color_map = plt.get_cmap(colormap)
        cNorm  = colors.Normalize(vmin, vmax)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=color_map)
        m = scalarMap      
        m.set_array(range(0, 1))
        plt.colorbar(m, orientation='horizontal')
        return scalarMap
    


class DrawModel(Draw):
    """
    
    """
    def __init__(self, model):
        self.model = model
        self.CrossSectionInSpace()

        
    def CrossSectionInSpace(self):
        """

        """
        title = 'Spatial distribution of facies and surfaces - {}'.format(self.model.Label)
        
        ax = self._MakePlot(title)
        for surface in self.model.Surfaces.values():
            DrawSurface(surface).draw(ax)
        for facies in self.model.Facies:
            DrawFacies(facies).draw(ax)
        plt.show()
        

class DrawFacies(object):
    def __init__(self, facies):
        self.Facies = facies
    
    
    def draw(self, ax):
        """
        
        """
        polygon =  self.Facies.Polygon
        col =  self.Facies.Color
        patch = PolygonPatch(polygon, facecolor=col, edgecolor='None', alpha=0.75, zorder=2)
        ax.add_patch(patch)
        
        

class DrawSurface(object):
    """
    """
    def __init__(self, surface):
        self.surface = surface
        
        
    def draw(self, ax):
        """
        
        """
        try:
            line = self.surface.Line
        except AttributeError:
            print(self.surface)
            raise
        if line.geom_type == "LineString":
            x, y = line.xy
            col = self.surface.Color
            ax.plot(x, y, color=col, alpha=0.75, linewidth=LINEWIDTH, solid_capstyle='round', zorder=2)
        elif line.geom_type == "MultiLineString":
            for line in line:
                x, y = line.xy
                col = self.surface.Color
                ax.plot(x, y, color=col, alpha=0.75, linewidth=LINEWIDTH, solid_capstyle='round', zorder=2)
        
     
        