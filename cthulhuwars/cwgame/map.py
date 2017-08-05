# coding=utf-8
from __future__ import print_function

"""
cthulhuWars
Map Class
Builds a network of map zones

TODO:
Replace string nodes with a zone class (TBD)
Add traversal methods
Flesh out graph visualization to represent class data
"""
ARNOLD = 0

import networkx as nx
import matplotlib.pylab as P
import matplotlib.image as mpimg
import numpy as np
import math as m
from .zone import Zone, GateState
import cthulhuwars.cwgame.color as Color
if ARNOLD:
    import cthulhuwars.cwgame.arnoldRender as arnoldRender
import pygame

import os

class Map:

    # Resolution
    width, height = 800, 400

    # available maps
    # Earth, 3 player, Eastern Hemisphere
    earth3PEH = {
        'Africa': ['South Atlantic', 'North Atlantic', 'Indian Ocean', 'Asia'],
        'Europe': ['Asia', 'Arctic Ocean', 'North Atlantic'],
        'Asia': ['North Pacific', 'Arctic Ocean', 'Europe', 'Africa', 'Indian Ocean', 'North Atlantic'],
        'Antarctica': ['South Atlantic', 'Indian Ocean'],

        'Arctic Ocean': ['Europe', 'Asia', 'North Atlantic'],
        'Indian Ocean': ['South Atlantic', 'Antarctica', 'Africa', 'Asia'],
        'North Atlantic': ['Arctic Ocean', 'South Atlantic', 'Europe', 'Africa'],
        'South Atlantic': ['North Atlantic', 'Antarctica', 'Indian Ocean', 'Africa'],
        'North Pacific': ['Asia', 'Arctic Ocean', 'Indian Ocean'],
    }

    # Earth, 3 player, Western Hemisphere
    earth3PWH = {
        'Europe': ['North Atlantic'],
        'North America': ['North Pacific', 'North Atlantic', 'Arctic Ocean', 'South America'],
        'South America': ['North America', 'North Pacific', 'South Pacific', 'North Atlantic', 'South Atlantic'],
        'Australia': ['Indian Ocean', 'South Pacific'],
        'Antarctica': ['South Atlantic', 'South Pacific'],

        'Arctic Ocean': ['North America', 'North Atlantic', 'North Pacific'],
        'Indian Ocean': ['South Atlantic', 'Antarctica', 'North Pacific', 'Australia', 'South Pacific'],
        'North Atlantic': ['Arctic Ocean', 'North Pacific', 'South Atlantic', 'North America', 'South America'],
        'South Atlantic': ['North Atlantic', 'Antarctica', 'Indian Ocean', 'South America', 'South Pacific'],
        'North Pacific': ['North America', 'Arctic Ocean', 'Indian Ocean', 'South America', 'South Pacific'],
        'South Pacific': ['North Pacific', 'Australia', 'South America', 'Antarctica', 'South Atlantic'],
    }

    # Earth, 5 player, Eastern Hemisphere
    earth5PEH = {
        'East Africa': ['South Atlantic', 'West Africa', 'Arabia', 'Indian Ocean'],
        'West Africa': ['North Atlantic', 'South Atlantic', 'East Africa', 'Arabia'],
        'Europe': ['Arabia', 'North Asia', 'North Atlantic', 'Scandinavia'],
        'Scandinavia': ['Arctic Ocean', 'North Atlantic', 'North Asia', 'Europe'],
        'Arabia': ['Europe', 'North Asia', 'South Asia', 'Indian Ocean', 'East Africa', 'West Africa'],
        'North Asia': ['North Pacific', 'Arctic Ocean', 'Europe', 'Scandinavia', 'Arabia', 'South Asia'],
        'South Asia': ['North Pacific', 'Indian Ocean', 'Arabia', 'North Asia'],
        'Antarctica': ['South Atlantic', 'Indian Ocean'],

        'Arctic Ocean': ['Scandinavia', 'North Asia', 'North Atlantic', 'North Pacific'],
        'North Pacific': ['Arctic Ocean', 'Indian Ocean', 'North Asia', 'South Asia'],
        'Indian Ocean': ['South Atlantic', 'Antarctica', 'North Pacific', 'East Africa', 'South Asia', 'Arabia'],
        'North Atlantic': ['Arctic Ocean', 'South Atlantic', 'West Africa', 'Arabia', 'Europe', 'Scandinavia'],
        'South Atlantic': ['North Atlantic', 'Antarctica', 'Indian Ocean', 'East Africa', 'West Africa']
    }

    # Earth, 5 player, Western Hemisphere
    earth5PWH = {
        'Europe':  ['North Atlantic'],
        'North America East': ['North Atlantic', 'Arctic Ocean', 'North America West'],
        'North America West': ['North America East', 'Central America', 'North Atlantic', 'North Pacific',
                               'Arctic Ocean'],
        'Central America': ['North America West', 'South America West', 'South America East', 'North Atlantic',
                            'North Pacific'],
        'South America East': ['South America West', 'Central America', 'North Atlantic', 'South Atlantic'],
        'South America West': ['Central America', 'South America East', 'South Pacific', 'North Pacific', ],
        'Australia': ['Indian Ocean', 'New Zealand'],
        'New Zealand': ['Australia', 'Indian Ocean', 'South Pacific'],
        'Antarctica': ['South Atlantic', 'South Pacific'],

        'Arctic Ocean': ['North America East', 'North America West', 'North Atlantic', 'North Pacific'],
        'North Pacific': ['Central America', 'North America West', 'Arctic Ocean', 'Indian Ocean',
                          'South America West', 'South Pacific'],
        'South Pacific': ['North Pacific', 'New Zealand', 'South America West', 'Antarctica', 'South Atlantic'],
        'Indian Ocean': ['South Atlantic', 'Antarctica', 'North Pacific', 'Australia', 'South Pacific', 'New Zealand'],
        'North Atlantic': ['North Pacific', 'South Atlantic', 'North America East', 'Central America',
                           'South America East', 'Europe', 'Arctic Ocean'],
        'South Atlantic': ['North Atlantic', 'Antarctica', 'South America East', 'South America West', 'South Pacific']
    }

    earth_oceans = ['Arctic Ocean', 'North Atlantic', 'South Atlantic', 'Indian Ocean', 'North Pacific',
                    'South Pacific']

    earth_gate_positions = {'Arctic Ocean': [0.03, 0.9], 'North Atlantic': [-0.23, 0.57],
                            'South Atlantic': [-0.05, 0.24], 'Indian Ocean': [0.69, 0.21],
                            'North Pacific':[-0.9, 0.54], 'South Pacific': [-0.53, 0.09],
                            'North America': [-0.58, 0.7], 'South America': [-0.33, 0.28],
                            'North America West': [-0.63, 0.75], 'North America East': [-0.36, 0.72],
                            'South America East': [-0.24, 0.31], 'South America West': [-0.4, 0.29],
                            'Central America': [-0.66, 0.55], 'Australia': [-0.9, 0.2],
                            'New Zealand': [-0.69, 0.25], 'Antarctica': [-0.025, 0.06],
                            'Africa': [0.21, 0.47], 'East Africa': [0.43, 0.25],
                            'West Africa': [0.21, 0.47], 'Europe': [0.37, 0.71],
                            'Scandinavia': [0.38, 0.87], 'Arabia': [0.56, 0.47], 'Asia': [0.68, 0.75],
                            'North Asia': [0.75, 0.79], 'South Asia': [0.85, 0.55]
                            }

    earth_map_configs = {'earth3P': ['earth3PWH', 'earth3PEH'], 'earth2Pa': ['earth5PWH', 'earth3PEH'],
                         'earth4Pa': ['earth5PWH', 'earth3PEH'], 'earth2Pb': ['earth3PWH', 'earth5PEH'],
                         'earth4Pb': ['earth3PWH', 'earth5PEH'], 'earth5P': ['earth5PWH', 'earth5PEH']
                         }

    # map_names = ['celaeno', 'dreamlands', 'earth', 'primeval earth', 'yuggoth']


    def __init__(self, num_players=3, map_name='earth3P', display=False):
        self.num_players = num_players
        self.map_name = map_name

        # we allow number of players and n-player map configurations to be in disagreement for experimentation
        west_map = {}
        east_map = {}

        if self.map_name == 'earth3P':
            west_map = self.earth3PWH
            east_map = self.earth3PEH

        if self.map_name == 'earth2Pa' or self.map_name == 'earth4Pa':
            west_map = self.earth5PWH
            east_map = self.earth3PEH

        if self.map_name == 'earth2Pb' or self.map_name == 'earth4Pb':
            west_map = self.earth3PWH
            east_map = self.earth5PEH

        if self.map_name == 'earth5P':
            west_map = self.earth5PWH
            east_map = self.earth5PEH

        # construct node graphs from dictionary of lists
        self._west_map = nx.from_dict_of_lists(west_map)
        self._east_map = nx.from_dict_of_lists(east_map)
        # construct combined node graph with compose()
        self.nx_map = nx.compose(self._east_map, self._west_map)
        self.nx_map.graph['name'] = self.map_name

        # relable nodes with zone objects
        node_list = self.nx_map.nodes()

        for node_name in node_list:
            is_ocean = False
            if node_name in self.earth_oceans:
                is_ocean = True
            self.nx_map.node[node_name]['zone'] = Zone(node_name, is_ocean)
            self.nx_map.node[node_name]['pos'] = [0.5, 0.5]
        # ^ map.nodes(data=True) will show the attributes of node label 'blah'
        '''
        # optionally, swap labeled nodes with name-tagged zone objects
        # warning: you might have to retype this to experiment
        # 'cos I may have drunkenly added some weird characters
        node_list = G.nodes()
        zone_list = []

        for node_name in node_list: 
            is_ocean = False 
            if node_name in self.earth_oceans: 
                is_ocean = True 
            zone_list.append(Zone(node_name, is_ocean))  
        mapping = dict(zip(node_list, zone_list))
         self.map = nx.relabel_nodes(G, mapping)
        '''
        self.basepath = '../cwgame/tex'
        self.imagepath = '.'
        self.file_format = '.png'
        self.west_map_filename = self.earth_map_configs[self.map_name][0] + self.file_format
        self.west_map_filename = os.path.join(self.basepath, self.west_map_filename)
        self.east_map_filename = self.earth_map_configs[self.map_name][1] + self.file_format
        self.east_map_filename = os.path.join(self.basepath, self.east_map_filename)

        self.display = display
        if display:
            pygame.init()
            # initialize the screen
            self.screen = pygame.display.set_mode((self.width, self.height))
            #self.clock = pygame.time.Clock()

            self.img_map_east = pygame.image.load(self.east_map_filename)
            self.img_map_west = pygame.image.load(self.west_map_filename)

            west = pygame.transform.smoothscale(self.img_map_west, (m.floor(self.width / 2), self.height))
            east = pygame.transform.smoothscale(self.img_map_east, (m.floor(self.width / 2), self.height))
            self.img_map_east = east.convert()
            self.img_map_west = west.convert()

            self.img_gate = pygame.image.load(os.path.join(self.basepath, 'gate.png'))
            self.img_gate = pygame.transform.smoothscale(self.img_gate, (32, 32))
            self.img_gate = self.img_gate.convert_alpha()


    def zone_by_name(self, zone):
        return self.nx_map.node[zone]['zone']

    def find_neighbors(self, zone, radius=1):
        if radius == 1:
            return self.nx_map.neighbors(zone)
        if radius == 2:
            ego_graph = nx.ego_graph(self.nx_map, zone, 2, center=False, undirected=True)
            return ego_graph.nodes()

    @property
    def eastMapImage(self):
        return self.east_map_filename

    @property
    def westMapImage(self):
        return self.west_map_filename

    def pygame_coords(self, x, y):
        x = int(x * (self.width * 0.5) + self.width * 0.5)
        y = int((1.0 - y) * (self.height))
        return (x, y)

    def show_map(self, save_image = False, image_prefix='image'):
        if self.display:
            self.screen.blit(self.img_map_west, (0, 0))
            self.screen.blit(self.img_map_east, (self.width / 2, 0))

            for node in self.nx_map.node:

                zone = self.nx_map.node[node]['zone']
                (x,y) = self.earth_gate_positions[zone.name]
                (x,y) = self.pygame_coords(x, y)

                if zone.gate_state != GateState.noGate:
                    self.screen.blit(self.img_gate, (x - 16, y - 16))
                i = 0
                for unit in zone.occupancy_list:
                    unit_x = x
                    if unit.gate_state != GateState.occupied:
                        unit_x = x + (i * 10)
                    pygame.draw.circle(self.screen, Color.NodeColorINT.FactionColor[str(unit.faction._faction.value)], (unit_x, y), 7, 0)
                    pygame.draw.circle(self.screen, (0, 0, 0), (unit_x, y), 8, 1)
                    i += 1

            if save_image:
                pygame.image.save(self.screen, image_prefix+self.file_format)


    def show_network_map(self, image_prefix='image'):

        img_west = mpimg.imread(self.west_map_filename)
        #print(img_west.shape)

        img_east = mpimg.imread(self.east_map_filename)
        #print(img_east.shape)

        img = np.concatenate((img_west, img_east), axis=1)

        P.imshow(img, extent=[-1, 1, 0, 1])

        #pos = nx.spring_layout(self.map, iterations=100)

        pos = {}
        cols = []
        for node in self.nx_map.node:
            cols.append(self.nx_map.node[node]['zone'].compute_color())
            pos[node] = self.earth_gate_positions[node]

        nx.draw(self.nx_map, pos, font_size=12, with_labels=False, node_color=cols)
        #for p in pos:  # raise text positions
        #    pos[p][1] += 0.07
        #nx.draw_networkx_labels(self.map, pos)
        img_name = self.imagepath+'/'+image_prefix+self.file_format
        P.savefig(img_name)
        #P.show()

    def render_map(self, image_prefix='image'):
        if ARNOLD:
            ar = arnoldRender.ArnoldRender(image_prefix)
            ar.do_render(1, self.nx_map)
        else:
            pass

    @property
    def empty_gates(self):
        results = []
        for node in self.nx_map.node:
            zone = self.nx_map.node[node]['zone']
            if zone.gate_state is GateState.emptyGate:
                results.append(zone)
        return results
