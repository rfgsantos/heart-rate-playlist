hrv = [] #list of strings with floats
track = ""
user = ""
location = ""
datetime = ""
reaction = {
    'user_id': user,
    'track_id': track,
    'location': location,
    'datetime': datetime,
    'heart_rate': hrv
}

processor = Processor()
processor.register_reaction(reaction)