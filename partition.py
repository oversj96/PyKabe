class Partition:
    def __init__(self, part_id):
        self.part_id = part_id
        self.bottom_segments = []
        self.top_segments = []
    
    
    def empty(self):
        return len(self.bottom_segments) == 0


    def initial_add(self, bot_id, top_id):
        self.bottom_segments.append(bot_id)
        self.top_segments.append(top_id)


    def add_top_id(self, top_id):
        self.top_segments.append(top_id)


    def add_bottom_id(self, bottom_id):
        self.bottom_segments.append(bottom_id)


    def bottom_id_exists(self, bot_id):
        if bot_id in self.bottom_segments:
            return True
        else: 
            return False

    def top_id_exists(self, top_id):
        if top_id in self.top_segments:
            return True
        else:
            return False

    def update(self, segment_id, top_segment_id):
        if self.bottom_id_exists(segment_id):
            self.add_top_id(top_segment_id)

        elif self.top_id_exists(top_segment_id):
            self.add_bottom_id(segment_id)
            
        elif self.empty():
            self.initial_add(segment_id, top_segment_id)


            

