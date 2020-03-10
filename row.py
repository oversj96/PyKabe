import schemes as sc
import segment as s
from part_tester import determine_part_set


class Row:


    def __init__(self, seed, length, partition_sets):
        self.seed = seed
        self.length = length
        self.partition_sets = partition_sets
        self.bits = []
        self.generate_bits()
        self.segments = []
        self.determine_segments()
        self.is_last_row = len(self.segments) == 0
        self.schemes = []
        if not self.is_last_row:
            self.generate_schemes()
        else:
            self.generate_last_row_schemes()
        

    def generate_bits(self):
        seed_copy = self.seed
        for i in range(self.length - 1, -1, -1):
            bitVal = 2**i
            if seed_copy >= bitVal:
                seed_copy -= bitVal
                self.bits.append(1)
            else:
                self.bits.append(0)
    

    def determine_segments(self):
        columns = []
        for i in range(0, len(self.bits)):
            if self.bits[i] == 0:
                columns.append(i)
                if i == len(self.bits) - 1:
                    self.segments.append(s.Segment(columns.copy()))
            elif self.bits[i] == 1 and len(columns) > 0:
                self.segments.append(s.Segment(columns.copy()))
                del columns[:]


    def generate_schemes(self):
        # Loop through the sets of a certain size of segments
        for scheme in self.partition_sets[len(self.segments)]:
            if max(scheme) == len(scheme) - 1:
                self.schemes.append(sc.RowScheme(self, self.segments, True, False, scheme))
            else:
                self.schemes.append(sc.RowScheme(self, self.segments, False, False, scheme))


    def generate_last_row_schemes(self):
        self.schemes.append(sc.RowScheme(self, self.segments, True, True, []))

    
    def forms_pool(self, other):
        for i in range(0, len(self.bits) - 1):
            if self.bits[i] == 0:
                if (self.bits[i] | other.bits[i] == 0) and (self.bits[i + 1] | other.bits[i + 1] == 0):
                    return True
        return False

    def is_trivially_contiguous(self, other):
        if self.is_last_row or other.is_last_row:
            return True
        # Deal with partitionless row case separate
        for i in range(0, len(self.bits)):
            if self.bits[i] == 0 and other.bits[i] == 0:
                return True
        return False
                    
    
def map_subrows(top, bottom):
    for top_scheme in top.schemes:
        key_set = determine_part_set(bottom, top_scheme)
        for bottom_scheme in bottom.schemes:
            # If the desired partition set is matched
            if key_set == bottom_scheme.partition_scheme:
                
                # Check if scheme succeeds
                if top_scheme.succeeds(bottom_scheme):
                    top_scheme.successors.append(bottom_scheme)

                # Check if scheme
                if top_scheme.finalizes(bottom_scheme):
                    top_scheme.finalizers.append(bottom_scheme)
    # 
    # if not top.forms_pool(bottom):
    #     for scheme in top.schemes:
    #         key_set = determine_part_set(bottom, scheme)
    #         for i in range(0, len(bottom.schemes)):
    #             if bottom.schemes[i].partition_scheme == key_set:
    #                 if scheme.is_contiguous_with(bottom.schemes[i]):
    #                     scheme.successors.append(bottom.schemes[i])   
    #                     if len(bottom.schemes[i].segments) == 1:
    #                         scheme.single_partition_successors.append(bottom.schemes[i])              
    #                         scheme.finalizers.append(bottom.schemes[i])
    #                     if len(set(scheme.partition_scheme)) <= 1 and not bottom.schemes[i].partition_scheme:
    #                         scheme.finalizers.append(bottom.schemes[i])
    #             else:
    #                 if not scheme.partition_scheme:
    #                     for i in range(0, len(bottom.schemes)):
    #                         if bottom.schemes[i].partition_scheme \
    #                         and max(bottom.schemes[i].partition_scheme) == len(bottom.schemes[i].partition_scheme) - 1:
    #                             scheme.successors.append(bottom.schemes[i])
    #                         else:
    #                             if not bottom.schemes[i].partition_scheme:
    #                                 scheme.successor.append(bottom.schemes[i])
    #                                 scheme.finalizers.append(bottom.schemes[i])

                                



    # def map_subrows(self, other):
    #     if not self.forms_pool(other):
    #         for self_subrow in self.schemes:
    #             for other_subrow in other.schemes:
    #                 key_set = build_part_set(other_subrow.parent_row, self_subrow)
    #                 if other_subrow.is_contiguous_with(self_subrow):
    #                     self_subrow.successors.append(other_subrow)
    #                     if len(other_subrow.partition_scheme) == 1:
    #                         self_subrow.finalizers.append(other_subrow)
