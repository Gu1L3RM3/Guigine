class SpatialHash:
    def __init__(self, cell_size=64):
        self.cell_size = cell_size
        self.cells = {}

    def _cell_id(self, x, y):
        return (x // self.cell_size, y // self.cell_size)

    def clear(self):
        self.cells.clear()

    def insert(self, entity, rect):
        cell_id = self._cell_id(rect.centerx, rect.centery)
        if cell_id not in self.cells:
            self.cells[cell_id] = []
        self.cells[cell_id].append((entity, rect))

    def query(self, rect):
        cx, cy = self._cell_id(rect.centerx, rect.centery)
        found = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                cell = self.cells.get((cx + dx, cy + dy))
                if cell:
                    found.extend(cell)
        return found
