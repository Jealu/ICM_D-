class Location(object):
    def __init__(self, _id, data):
        self.id = _id
        self.block = data[3]
        self.type = data[2]  # 1: suitable for destination charge / 0: otherwise
        self.x = data[0]
        self.y = data[1]
        self.super_charge_num = 0
        self.destination_charge_num = 0

    pass
