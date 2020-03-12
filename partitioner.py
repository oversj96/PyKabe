import segment
from partition import Partition as part


class Partitioner:
    def __init__(self, bottom_row, top_row_scheme):
        self.top_scheme = top_row_scheme
        self.bottom_row = bottom_row
        self.partitions = []
        self.bottom_row_ids = [i for i in range(0, len(self.bottom_row.segments))]
        if self.bottom_row_ids:
            self.partition_bottom_row()
            self.scheme = self.part_scheme()
        elif len(self.bottom_row.segments) == 0:
            self.scheme = []


    def partition_bottom_row(self):
        for i in range(0, len(self.bottom_row.segments)):
            p = part(i)

            for j in range()
            
        #     for j in range(0, len(self.bottom_row.segments)):
        #         for k in range(0, len(self.top_scheme.segments)):
        #             if self.bottom_row.segments[j].connects(self.top_scheme.segments[k]):
        #                 if len(self.bottom_row_ids) == 0:
        #                     break
        #                 else:
        #                     if j in self.bottom_row_ids:
        #                         key = self.bottom_row_ids.pop(self.bottom_row_ids.index(j))
        #                         p.update(key, k)       
        #             # If there is no top segment this bottom segment connects to
        #             if k == len(self.top_scheme.segments) - 1 and j in self.bottom_row_ids:
        #                 key = self.bottom_row_ids.pop(self.bottom_row_ids.index(j))
        #                 p.update(key, -1)           
        #     self.partitions.append(p)


    def matching_top_partition_segments(self, part_id):
        return [i for i in range(0, len(self.top_scheme.segments)) if self.top_scheme.partition_scheme[i] == part_id]


    def part_scheme(self):
        scheme = [-1 for i in range(0, len(self.bottom_row.segments))]
        changed = [False for i in range(0, len(self.bottom_row.segments))]

        for i in range(0, len(self.partitions)):
            if len(self.partitions[i].top_segments) != 0:
                for seg_id in self.partitions[i].bottom_segments:
                    if not changed[seg_id]:
                        scheme[seg_id] = self.partitions[i].part_id
                        changed[seg_id] = True
            else:
                if not changed[i]:
                    scheme[i] = i

        return scheme
