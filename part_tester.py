import segment as s


def build_part_set(bottom_row, top_row_scheme):
    if not top_row_scheme.partition_set or len(bottom_row.segments) == 0:
        return []
    # Construct a new partiton set to be used
    new_set = [i for i in range(0, len(bottom_row.segments))]
    # For each segment in the bottom row...
    for i in range(0, len(bottom_row.segments)):
        # ...for each segment in the top row...
        for j in range(0, len(top_row_scheme.segments)):
            # determine of the bottom row connects to the top
            if bottom_row.segments[i].connects(top_row_scheme.segments[j]):
                # If it does, the new partition set is updated with the number
                new_set[i] = top_row_scheme.partition_set[j]
            
            else:
                if len(bottom_row.segments) > len(top_row_scheme.parent_row.segments):
                    for k in range(i, len(top_row_scheme.partition_set)):
                        top_row_scheme.partition_set[k] += 1

    for i in range(0, len(set(top_row_scheme.partition_set)) - 1):
        key = new_set[i]
        for j in range(i, len(new_set)):
            if new_set[j] == key:
                new_set[j] = i

    return new_set



def map_part_set(top_row_scheme, bottom_row):
    '''Given a top row bitset, a top row partition scheme, and a bottom row bitset, return
    the bottom row scheme.'''
    if len(bottom_row.segments) == 0:
        return []

    elif len(top_row_scheme.parent_row.segments) == 0:
        return [i for i in range(0, len(bottom_row.segments))]

    # The horror. Begin a long process of partition matching. Documentation coming soon.
    # Easily some of the worst code I've written, but it was the only way I could figure
    # out how to make this work.
    else:
        bottom_partition = [len(bottom_row.segments) for i in range(0, len(bottom_row.segments))]
        top_partition = top_row_scheme.partition_set.copy()
        
        reachable_bottom_seg_ids = []
        partition_set = sorted(set(top_row_scheme.partition_set))
        for partition in partition_set:
            seg_ids = []
            for i in range(0, len(top_row_scheme.segments)):
                if top_row_scheme.partition_set[i] == partition:
                    for j in range(0, len(bottom_row.segments)):
                        if top_row_scheme.segments[i].connects(bottom_row.segments[j]):
                            seg_ids.append(j)
            reachable_bottom_seg_ids.append(seg_ids.copy())

        visited = [False for i in range(0, len(bottom_row.segments))]
        isolated = [False for i in range(0, len(bottom_row.segments))]
        for i in range(0, len(bottom_row.segments)):
            for j in range(0, len(top_row_scheme.segments)):
                if top_row_scheme.segments[j].connects(bottom_row.segments[i]):
                    isolated[i] = False
                    break

        min_vals = []
        for i in range(0, len(reachable_bottom_seg_ids)):
            min_val = 100
            for seg_id in reachable_bottom_seg_ids[i]:
                if min_val > seg_id:
                    min_val = seg_id
            for j in range(0, len(reachable_bottom_seg_ids[i])):
                if not visited[reachable_bottom_seg_ids[i][j]]:
                    bottom_partition[reachable_bottom_seg_ids[i][j]] = min_val
                    visited[reachable_bottom_seg_ids[i][j]] = True

        used_numbers = [i for i in range(len(bottom_partition), -1, -1)]
        for i in range(0, len(bottom_partition)):
            if i <= bottom_partition[i]:
                key = bottom_partition[i]
                repl = used_numbers.pop()
                for j in range(i, len(bottom_partition)):
                    if bottom_partition[j] == key:
                        bottom_partition[j] = repl
                    else:
                        if bottom_partition[j] >= repl:
                            bottom_partition[j] += 1
        
        return bottom_partition


def build_part_set(top_node, bottom_row):
    if len(bottom_row.segments) == 0:
        return []

    elif len(top_node.parent_row.segments) == 0:
        return [i for i in range(0, len(bottom_row.segments))]

    else:
        top_parts =  top_node.partition_set

        connective_list = []
        for i in range(0, len(bottom_row.segments)):
            connections  = []
            for j in range(0, len(top_parts)):
                if bottom_row.segments[i].connects(top_node.segments[j]):
                    connections.append(top_parts[j])
            connective_list.append(connections.copy())

        min_vals = []
        for i in range(0, len(connective_list)):
            if len(connective_list[i]) != 0:
                min_vals.append(min(connective_list[i]))
            else:
                min_vals.append(-1)

        for i in range(0, len(min_vals)):
            if min_vals[i] != None and min_vals[i] > 0:
                j = 0
                while j < len(connective_list):
                    if j != i:
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

        for i in range(0, len(locations_of_seen)):
            for loc in locations_of_seen[i]:
                min_vals[loc] = i
            
        return min_vals





def determine_segments(row):
    seg_list = []
    columns = []
    for i in range(0, len(row)):
        if row[i] == 0:
            columns.append(i)
            if i == len(row) - 1:
                seg_list.append(s.Segment(columns.copy()))
        elif row[i] == 1 and len(columns) > 0:
            seg_list.append(s.Segment(columns.copy()))
            del columns[:]
    return seg_list


if __name__ == "__main__":
    pass
    # length = 4
    # part_schemes = [rgs(i) for i in range(0, length + 1)]
    # r1 = r.Row(10, length, part_schemes)
    # r2 = r.Row(3, length, part_schemes)
    # scheme = r1.schemes[1]

    # print(build_part_set(r1, scheme))
