import core_engine
from datetime import datetime, timedelta

processor = core_engine.Processor()

def handle_new_user(code):
    expiration_time = datetime.now() + timedelta(hours=1)
    expiration_time = expiration_time.strftime("%Y-%m-%d %H:%M:%S")
    processor.register_user(code, expiration_time)

def handle_new_reaction(reaction):
    processor.register_reaction(reaction)