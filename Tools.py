class Tools(object):
    def __init__(self):
        self.name = 'tool_box'

    def read_flow_data_from_txt(self):
        xf = open('scaled_x.csv', 'r')
        yf = open('scaled_y.csv', 'r')
        xlines = xf.readlines()
        x_split = [l.split(', ') for l in xlines]
        ylines = yf.readlines()
        y_split = [l.split(', ') for l in ylines]
        flow_data = []
        for i in xrange(len(x_split)):
            flow = [[float(x_split[i][j]), float(y_split[i][j])] for j in xrange(len(x_split[i])) if len(x_split[i][j])>2]
            flow_data.append(flow)
        xf.close()
        yf.close()
        return flow_data

    def read_loc_data_from_txt(self):
        f = open('1.csv', 'r')
        lins = f.readlines()
        loc_split = [l.split(',') for l in lins]
        loc_data = []
        for i in xrange(len(loc_split)):
            loc = [float(data) for data in loc_split[i]]
            loc_data.append(loc)
        f.close()
        return loc_data

    def read_slot_data_from_txt(self):
        f = open('time.txt', 'r')
        lines = f.readlines()
        time_data = [int(l) for l in lines]
        f.close()
        return time_data