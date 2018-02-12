from Track import *
from Location import *
import random


class Scenario(object):
    def __init__(self, flow_data, location_data, slot_data):
        self.location_threshold = [94, 155, 250, 294, 385, 424, 660, 788, 868]
        self.track_list = [Track(i, flow_data[i], slot_data[i]) for i in xrange(len(flow_data))]
        self.location_list = [Location(i, location_data[i]) for i in xrange(len(location_data))]
        self.calculate_locs()

    def calculate_locs(self):
        for track in self.track_list:
            for point in track.point_list:
                dist_list = [abs(point.x-loc.x)+abs(point.y-loc.y) for loc in self.location_list]
                track.feasible_slow_locations = [i for i in xrange(len(dist_list)) if (dist_list[i]<0.009 and self.location_list[i].type >0 )]
                track.feasible_super_locations = [i for i in xrange(len(dist_list)) if dist_list[i]<0.009]
        track_to_remove = []
        for track in self.track_list:
            if len(track.feasible_slow_locations)+len(track.feasible_super_locations) == 0:
                track_to_remove.append(track)
        for track in track_to_remove:
            self.track_list.remove(track)

    def generate_initial_solution(self):
        result = []
        for i in xrange(48):
            genes = [0 for j in xrange(len(self.location_list))]
            flow_in_slot = [f for f in self.track_list if f.time_slot==i]
            for f in flow_in_slot:
                loc = random.choice(f.feasible_slow_locations+f.feasible_super_locations)
                genes[loc] += 1
            result.append(genes)
        gene = [0 for j in xrange(len(self.location_list))]
        for i in xrange(len(self.location_list)):
            gene[i] = max([g[i] for g in result])
        gene_s = [str(g)+'\n' for g in gene]
        f = open('input.txt', 'w')
        f.writelines(gene_s)
        f.close()