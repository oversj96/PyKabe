import segment as s
from node import Node


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
            bitVal = 2 ** i
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
                self.nodes.append(
                    Node(self, self.segments, True, False, partition_set)
                )
            else:
                self.nodes.append(
                    Node(self, self.segments, False, False, partition_set)
                )

    def generate_last_row_nodes(self):
        self.nodes.append(Node(self, self.segments, True, True, []))

    def forms_pool(self, other):
        for i in range(0, len(self.bits) - 1):
            if self.bits[i] == 0:
                if (self.bits[i] | other.bits[i] == 0) and (
                    self.bits[i + 1] | other.bits[i + 1] == 0
                ):
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
    # Every node needs to be mapped to every other node
    # This is intrinsically a O(n^2) operation.
    for top_node in top.nodes:
        # Mapping the set is also a at worst
        # case O(n^3) operation. This is where most processing time
        # is spent while building the tree.
        legal_set = map_set(top_node, bottom)
        for bottom_node in bottom.nodes:
            # If the desired partition set is matched
            # Linear search for the legal set in the bottom node
            if legal_set == bottom_node.partition_set:

                # Check if node is_inode
                if top_node.is_inode(bottom_node):
                    top_node.inodes.append(bottom_node)

                # Check if node is a terminal/leaf node
                if top_node.is_leaf_node(bottom_node):
                    top_node.leaf_nodes.append(bottom_node)
                # Once we've found a matching node there's no point
                # in continuing the search, so we break.
                break


def map_set(top_node, bottom_row):
    """Maps a partition set for the bottom row given the top partition
     set, the bottom row segments, and the top row segments."""

    # If there are no segments in the bottom row
    if len(bottom_row.segments) == 0:
        return []

    # If there are no segments in the top row
    elif len(top_node.parent_row.segments) == 0:
        return [i for i in range(0, len(bottom_row.segments))]

    # Otherwise, we must create a legal bottom partition set given
    # the partition set of the top and the segments for both.
    else:
        # For easier debugging and use, put the part set
        # in its own variable.
        top_parts = top_node.partition_set

        # For every segment in the bottom determine what
        # segments, and their subsequent partition numbers,
        # can be reached by them.
        connective_list = []
        for i in range(0, len(bottom_row.segments)):
            connections = []
            for j in range(0, len(top_parts)):
                if bottom_row.segments[i].connects(top_node.segments[j]):
                    connections.append(top_parts[j])
            connective_list.append(connections.copy())

        # We only want to keep the smallest partition number
        # available to each segment
        min_vals = []
        for i in range(0, len(connective_list)):
            if len(connective_list[i]) != 0:
                min_vals.append(min(connective_list[i]))
            else:
                min_vals.append(-1)

        # Now we expand the scope of each segment,
        # ensuring that if a segment is connected somehow to a
        # smaller partition number, it will find it.
        # This portion of the code is what needs optimizing the most.
        for i in range(0, len(min_vals)):
            if min_vals[i] != None and min_vals[i] > 0:
                j = 0
                while j < len(connective_list):
                    if j != i:
                        # This linear search can be done at worst n times,
                        # making this function O(n^3)
                        if min_vals[i] in connective_list[j]:
                            context_min = min(connective_list[j])
                            if context_min != min_vals[i]:
                                min_vals[i] = context_min
                                j = 0
                            else:
                                j += 1
                        else:
                            j += 1
                    else:
                        j += 1

        # Set -1 vals to unique partition
        for i in range(0, len(min_vals)):
            if min_vals[i] == -1:
                min_vals[i] = max(min_vals) + 1

        # Reorders the partition sets so that they can match with
        # the restrictive growth strings that we are using for
        # partitioning.
        seen = []
        locations_of_seen = []
        for i in range(0, len(min_vals)):
            if min_vals[i] not in seen:
                seen.append(min_vals[i])
                locations = []
                for j in range(0, len(min_vals)):
                    if min_vals[j] == min_vals[i]:
                        locations.append(j)
                locations_of_seen.append(locations.copy())

        # Goes with the above block of code, orders partitions
        # uniquely in restrictive growth string fashion.
        for i in range(0, len(locations_of_seen)):
            for loc in locations_of_seen[i]:
                min_vals[loc] = i

        # Whats left should be the legal set that maps to the bottom row from the top node.
        # This set plus the bottom row will make a potential child node for the top node.
        return min_vals
