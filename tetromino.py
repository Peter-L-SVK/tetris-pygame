import random

class Tetromino:
    SHAPES = [
        [[1, 1, 1, 1]],  # I
        [[1, 0, 0], [1, 1, 1]],  # J
        [[0, 0, 1], [1, 1, 1]],  # L
        [[1, 1], [1, 1]],  # O
        [[0, 1, 1], [1, 1, 0]],  # S
        [[0, 1, 0], [1, 1, 1]],  # T
        [[1, 1, 0], [0, 1, 1]]   # Z
    ]
    
    COLORS = [
        (0, 255, 255),  # Cyan - I
        (0, 0, 255),    # Blue - J
        (255, 165, 0),  # Orange - L
        (255, 255, 0),  # Yellow - O
        (0, 255, 0),    # Green - S
        (128, 0, 128),  # Purple - T
        (255, 0, 0)     # Red - Z
    ]

    def __init__(self, shape_idx=None, grid_width=10):
        self.shape_idx = random.randint(0, len(self.SHAPES) - 1) if shape_idx is None else shape_idx
        self.shape = self.SHAPES[self.shape_idx]
        self.color = self.COLORS[self.shape_idx]
        self.x = grid_width // 2 - len(self.shape[0]) // 2
        self.y = 0
    
    def rotate(self):
        """Rotate the tetromino 90 degrees clockwise"""
        rotated = [[self.shape[y][x] for y in range(len(self.shape))] 
                  for x in range(len(self.shape[0]) - 1, -1, -1)]
        return rotated
