import sys

import row
import segment as s
from Debugger.matrix import Matrix


class Node:

    debug_count = 0
    recursion_calls = 0
    current_seed = 0

    def __init__(
        self, parent_row, segments, is_start, is_partitionless, partition_set
    ):
        self.parent_row = parent_row
        self.bits = self.parent_row.bits
        self.segments = segments
        self.is_start = is_start
        self.partition_set = partition_set
        self.depth_memoized = []
        self.memos = []
        self.inodes = []
        self.leaf_nodes = []
        self.is_partitionless = is_partitionless

    def is_inode(self, other):
        # If partitionless scheme
        if self.is_partitionless:
            if other.is_partitionless:
                return True
            elif max(other.partition_set) == len(other.partition_set) - 1:
                return True

        # If single partition scheme
        elif len(set(self.partition_set)) == 1:
            if other.is_partitionless:
                return True
            else:
                return self.connects_all_partitions(other)

        # If multipart scheme
        elif len(set(self.partition_set)) > 1:
            if other.is_partitionless:
                return False
            else:
                return self.connects_all_partitions(other)

        # Any other case not handled is invalid or incorrectly handled, potentially.
        else:
            return False

    def is_leaf_node(self, other):
        # If partitionless scheme
        if self.is_partitionless:
            # Only partitionless or single partition set is allowed.
            if other.is_partitionless:
                return True
            elif len(other.segments) == 1:
                return True

        # If single partition scheme
        elif len(set(self.partition_set)) == 1:
            if other.is_partitionless:
                return True
            else:
                if len(set(other.partition_set)) == 1:
                    return self.connects_all_partitions(other)

        # If multipart scheme
        elif len(set(self.partition_set)) > 1:
            # Only single partition set is allowed
            if len(set(other.partition_set)) == 1:
                return self.connects_all_partitions(other)

        return False

    def connects_all_partitions(self, other):
        """This function assumes both schemes possess segments and are not the partitionless scheme."""
        try:
            if self.is_partitionless or other.is_partitionless:
                raise ValueError(
                    "One of the rows was the partitionless scheme!"
                )
            connections = [False for i in range(0, len(self.partition_set))]
            for i in range(0, len(self.segments)):
                for j in range(0, len(other.segments)):
                    if not connections[i]:
                        if self.segments[i].connects(other.segments[j]):
                            connections[i] = True

            # Maybe source of error, I'm tired while writing this.
            for i in range(0, len(connections)):
                if connections[i]:
                    key = self.partition_set[i]
                    for j in range(0, len(connections)):
                        if self.partition_set[j] == key:
                            connections[j] = True
            # If there is a false in the bool vector connections, this will return False.
            return not False in connections
        except ValueError as ve:
            print(ve)

    def traverse_with_memoization(self, water, end, depth, base_depth):
        # If the subrow memo vector has not been initialized for the puzzle depth
        if not self.depth_memoized:
            Node.recursion_calls += 1
            self.depth_memoized = [False for i in range(0, base_depth)]
            self.memos = [0 for i in range(0, base_depth)]

        if depth == 1:
            sys.stdout.write(
                f"\rCounting using memoization... {(self.parent_row.seed / 2**self.parent_row.length) * 100:.2f}%"
                + " " * 20
            )

        count = 0

        if end:
            if depth == base_depth - 1:
                count += 1
            else:
                count += self.traverse_with_memoization(
                    water, end, depth + 1, base_depth
                )

        # If the current depth for this subrow has not been counted
        elif not self.depth_memoized[depth - 1]:

            # Puzzle has reached the row before the last and considers the final row placements.
            if depth == base_depth - 1:
                for leaf_node in self.leaf_nodes:

                    # If the next row is the final row, just count the leaf nodes.
                    count = len(self.leaf_nodes)

            elif depth != base_depth - 1:

                if not water:
                    for inode in self.inodes:
                        if inode.is_start:
                            has_water = len(inode.segments) >= 1
                            count += inode.traverse_with_memoization(
                                has_water, end, depth + 1, base_depth
                            )

                else:
                    for inode in self.inodes:
                        if inode.is_partitionless:
                            is_end = True
                        else:
                            is_end = False
                        count += inode.traverse_with_memoization(
                            water, is_end, depth + 1, base_depth
                        )
            else:
                print("breakpoint print out")

            # Make it known this depth has been counted for this subrow
            self.depth_memoized[depth - 1] = True
            # Assign the count to this subrows depth level
            self.memos[depth - 1] = count
        # If this depth has already been counted
        else:
            count = self.memos[depth - 1]

        # print(f"Seed: {self.parent_row.seed}, Depth: {depth}, Count: {count}")
        return count

    def traverse(self, string, water, end, depth, base_depth):
        Node.recursion_calls += 1
        """Traverses without memoizing, but allows for pattern printouts as a trade off."""
        string[depth - 1] = self.parent_row

        if depth == 1:
            Node.current_seed = self.parent_row.seed

        # Keep track of count at this node, always starts at zero
        count = 0

        if end:
            if depth == base_depth - 1:
                string[depth] = self.parent_row
                self.print_puzzle(string)
                count += 1
            else:
                count += self.traverse(
                    string, water, end, depth + 1, base_depth
                )

        # Puzzle has reached the row before the last and considers the final row placements.
        elif depth == base_depth - 1:
            for leaf_node in self.leaf_nodes:

                # If forced end is set to True
                if end:
                    if leaf_node.is_partitionless:
                        string[depth] = leaf_node.parent_row
                        self.print_puzzle(string)
                        count += 1
                else:
                    string[depth] = leaf_node.parent_row
                    self.print_puzzle(string)
                    count += 1

        elif depth != base_depth - 1:

            if not water:
                for inode in self.inodes:
                    if inode.is_start:
                        has_water = len(inode.segments) >= 1
                        count += inode.traverse(
                            string, has_water, end, depth + 1, base_depth
                        )

            else:
                for inode in self.inodes:
                    if inode.is_partitionless:
                        is_end = True
                    else:
                        is_end = False
                    count += inode.traverse(
                        string, water, is_end, depth + 1, base_depth
                    )
        else:
            print("breakpoint print out")

        return count

    def print_puzzle(self, string):
        length = len(string[0].bits)
        depth = len(string)
        Node.debug_count += 1
        debug_interval = 50
        if Node.debug_count % debug_interval == 0:

            sys.stdout.write(
                f"\rCounting with debugger... {(Node.current_seed / 2**self.parent_row.length) * 100:.2f}%"
                + f"  Puzzles Count: {Node.debug_count:,}"
                + f"  Puzzles Manually Tested: {Node.debug_count // debug_interval:,}"
            )
            sys.stdout.flush()

            rows = [string[i].bits for i in range(0, len(string))]
            mat = Matrix(
                self.parent_row.length, Node.debug_count, rows, [], "none"
            )
            if mat.water_count > 0:
                mat.test_puzzle(
                    mat.first_water_point[0], mat.first_water_point[1], 1
                )

                if mat.problem_type == "Illegal Puzzle":
                    sys.stdout.write(
                        f"\n!! Illegal Puzzle Warning !!\n"
                        + f"Puzzle Seed: {mat.matrix_seed}\n"
                        + f"Debug Count: {Node.debug_count}\n"
                        + f"See output file for this matrix size for more info.\n"
                    )
                    with open(
                        f"debug\\debug_[{depth}x{length}].txt", "a"
                    ) as file:

                        file.write(f"{Node.debug_count}\n")
                        for row in string:
                            for bit in row.bits:
                                if bit == 1:
                                    file.write("1 ")
                                else:
                                    file.write(f"0 ")
                            file.write(f"  {row.seed}\n")
                        file.write("\n")
