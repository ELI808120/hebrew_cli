import os
def execute(args):
    return {"lines": [{"text": f"משתמש נוכחי: {os.getlogin()}", "type": "success"}]}