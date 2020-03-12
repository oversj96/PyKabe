class SegmentCrawler:
    def __init__(self, bottom_segments, top_segments, top_scheme):
        self.bottom_segments = bottom_segments
        self.top_segments = top_segments
        self.top_scheme = top_scheme
        self.itinerary = []
        self.partitions = []

    def crawl(self, path, top_cursor, bottom_cursor, side):
        if not self.bottom_segments:
            return []
        else:
            if side == 'top':
                path[1].append(top_cursor)
            else:
                path[0].append(bottom_cursor)
