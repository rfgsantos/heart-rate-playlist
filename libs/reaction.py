

class Reaction:
    def __init__(self):
        self.track_id = ""
        self.track_duration = 0
        self.reaction_id = -1
        self.reaction = []
        self.hrv = None
        self.reaction_duration = self._reaction_duration()
    
    def _reaction_duration(self):
        return sum(self.reaction)