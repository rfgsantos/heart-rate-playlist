import sys
sys.path.append("../")
from util.hrv import *

class Reaction:
    def __init__(self, track_id, track_duration, reaction_id, reaction):
        self.track_id = track_id
        self.track_duration = track_duration
        self.reaction_id = reaction_id
        self.reaction = reaction
        self.hrv = self._reaction_hrv()
        self.reaction_duration = self._reaction_duration()
    
    def _reaction_duration(self):
        try:
            return self.reaction[-1]/1000
        except:
            print("No HRV.")
            return 0

    def _reaction_hrv(self):
        try:
            str_reaction = self.reaction.split(",")
            self.reaction = [float(rr) for rr in str_reaction]
            return hrv(self.reaction, 1000)
        except ValueError:
            print("ValueError.")
            return None