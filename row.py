import segment as s
from node import Node
from part_tester import build_part_set as bps


class Row:
    def __init__(self, seed, length, partition_sets):
        self.seed = seed
        self.length = length
        self.set_of_partition_sets = partition_sets
        self.bits = []
        self.generate_bits()
        self.segments = []
        self.determine_segments()
        self.is_partitionless_row = len(self.segments) == 0
        self.nodes = []
        if not self.is_partitionless_row:
            self.generate_nodes()
        else:
            self.generate_last_row_nodes()
        

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


    def generate_nodes(self):
        # Loop through the sets of a certain size of segments
        for partition_set in self.set_of_partition_sets[len(self.segments)]:
            if max(partition_set) == len(partition_set) - 1:
                self.nodes.append(Node(self, self.segments, True, False, partition_set))
            else:
                self.nodes.append(Node(self, self.segments, False, False, partition_set))


    def generate_last_row_nodes(self):
        self.nodes.append(Node(self, self.segments, True, True, []))

    
    def forms_pool(self, other):
        for i in range(0, len(self.bits) - 1):
            if self.bits[i] == 0:
                if (self.bits[i] | other.bits[i] == 0) and (self.bits[i + 1] | other.bits[i + 1] == 0):
                    return True
        return False


    def is_trivially_contiguous(self, other):
        if self.is_partitionless_row or other.is_partitionless_row:
            return True
        # Deal with partitionless row case separate
        for i in range(0, len(self.bits)):
            if self.bits[i] == 0 and other.bits[i] == 0:
                return True
        return False
                    
    
def build_tree(top, bottom):
    for top_node in top.nodes:
        legal_set = bps(top_node, bottom)
        for bottom_node in bottom.nodes:
            # If the desired partition set is matched
            if legal_set == bottom_node.partition_set:
                
                # Check if node is_inode
                if top_node.is_inode(bottom_node):
                    top_node.inodes.append(bottom_node)

                # Check if node
                if top_node.is_leaf_node(bottom_node):
                    top_node.leaf_nodes.append(bottom_node)
    #       
                break
    # if not top.forms_pool(bottom):
    #     for node in top.nodes:
    #         key_set = determine_part_set(bottom, node)
    #         for i in range(0, len(bottom.nodes)):
    #             if bottom.nodes[i].partition_node == key_set:
    #                 if node.is_contiguous_with(bottom.nodes[i]):
    #                     node.inodes.append(bottom.nodes[i])   
    #                     if len(bottom.nodes[i].segments) == 1:
    #                         node.single_partition_inodes.append(bottom.nodes[i])              
    #                         node.leaf_nodes.append(bottom.nodes[i])
    #                     if len(set(node.partition_node)) <= 1 and not bottom.nodes[i].partition_node:
    #                         node.leaf_nodes.append(bottom.nodes[i])
    #             else:
    #                 if not node.partition_node:
    #                     for i in range(0, len(bottom.nodes)):
    #                         if bottom.nodes[i].partition_node \
    #                         and max(bottom.nodes[i].partition_node) == len(bottom.nodes[i].partition_node) - 1:
    #                             node.inodes.append(bottom.nodes[i])
    #                         else:
    #                             if not bottom.nodes[i].partition_node:
    #                                 node.successor.append(bottom.nodes[i])
    #                                 node.leaf_nodes.append(bottom.nodes[i])

                                



    # def map_subrows(self, other):
    #     if not self.forms_pool(other):
    #         for self_subrow in self.nodes:
    #             for other_subrow in other.nodes:
    #                 key_set = build_part_set(other_subrow.parent_row, self_subrow)
    #                 if other_subrow.is_contiguous_with(self_subrow):
    #                     self_subrow.inodes.append(other_subrow)
    #                     if len(other_subrow.partition_node) == 1:
    #                         self_subrow.leaf_nodes.append(other_subrow)
