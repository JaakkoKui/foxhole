class Segis:
    """
    Segis is a points system for the game, ranging from 0 to 100.
    Points increase on win, decrease over time, and can be imported and used in other modules.
    """

    def __init__(self, initial=20):
        self.value = max(0, min(100, initial))

    def add(self, amount):
        self.value = min(100, self.value + amount)

    def subtract(self, amount):
        self.value = max(0, self.value - amount)

    def update(self, dt, decay_rate=0.01):
        """
        Call this every frame with dt (milliseconds) to reduce segis over time.
        decay_rate: points lost per second.
        """
        self.subtract(decay_rate * (dt / 1000))

    def get(self):
        return int(self.value)
