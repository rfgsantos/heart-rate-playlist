import sys
sys.path.append("../")
sys.path.append("../libs/")
from libs.core_engine import *

p = Processor("../configs/credentials.json")
for user in p.get_users():
    print("\n", user.id)
    print("\n", user.access_token)
    print("\n", user.refresh_token)
    if user.reactions:
        for reaction in user.reactions:
            print("\n", reaction.track_id)
            print("\n", reaction.track_duration)
            print("\n", reaction.reaction_duration)
            print("\n", reaction.reaction_id)
            if reaction.hrv:
                print("\n", reaction.hrv[0])
            
    print(user.positive_reaction())