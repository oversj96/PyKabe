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

        


    





def determine_part_set(bottom_row, top_row_scheme):

    part_hit = [None for i in range(0, len(bottom_row.segments))]

    for i in range(0, len(bottom_row.segments)):
        for j in range(0, len(top_row_scheme.segments)):
            if bottom_row.segments[i].connects(top_row_scheme.segments[j]):
                part_hit[i] = top_row_scheme.partition_set[j]
    
    new_set = [-1 for i in range(0, len(bottom_row.segments))]
    changed = [False for i in range(0, len(bottom_row.segments))]
    for i in range(0, len(bottom_row.segments)):
        next_part_num = max(new_set) + 1
        if part_hit[i] == None:
            new_set[i] = next_part_num
        else:
            key = part_hit[i]
            for j in range(i, len(bottom_row.segments)):
                if part_hit[j] == key and not changed[j]:
                    new_set[j] = next_part_num
                    changed[j] = True

    return new_set if -1 not in new_set else print(f"Error: set with -1 detected! Seed: {bottom_row.parent_row.seed}")



    



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
