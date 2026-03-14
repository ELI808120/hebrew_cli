import os
def execute(args):
    files = [f[:-3] for f in os.listdir('commands') if f.endswith('.py')]
    return {"lines": [{"text": "הפקודות המותקנות במערכת:", "type": "success"}, {"text": ", ".join(files), "type": ""}]}