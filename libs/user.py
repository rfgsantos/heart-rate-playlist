class User:
    def __init__(self, id, atk, rtk):
        self.id = id
        self.refresh_token = rtk
        self.access_token = atk
        self.reactions = []

    def positive_reactions(self):
        positives = []
        for reaction in self.reactions:
            if reaction.reaction_duration > float(reaction.track_duration) * 0.10:
                positives.append(reaction.track_id)
        return positives