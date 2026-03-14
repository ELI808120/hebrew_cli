import time
def execute(args):
    return {"lines": [{"text": f"השעה כעת: {time.strftime('%H:%M:%S')}", "type": "success"}]}