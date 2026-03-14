import platform
def execute(args):
    return {"lines": [{"text": f"מערכת הפעלה: {platform.system()} {platform.release()}", "type": "success"}]}