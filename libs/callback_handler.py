import core_engine
from datetime import datetime, timedelta

processor = core_engine.Processor()

def handle_new_user(code):
    expires_at = datetime.now() + timedelta(hours=1)
    expires_at = expires_at.strftime("%Y-%m-%d %H:%M:%S")
    processor.register_user(code, expiration_time)

def handle_new_reaction(information):
    #handle information
    processor.register_reaction(information)