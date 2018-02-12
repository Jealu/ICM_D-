from Point import *


class Track(object):
    def __init__(self, _id, track_data, slot):
        self.id = _id
        self.point_list = [Point(data[0], data[1]) for data in track_data]
        self.time_slot = slot
        self.feasible_slow_locations = []
        self.feasible_super_locations = []

    pass
