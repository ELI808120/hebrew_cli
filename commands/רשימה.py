import os

def execute(args):
    lines = [{"text": "--- תוכן התיקייה ---", "type": "success"}]
    for f in os.listdir('.'):
        prefix = "📁 [תיקייה]" if os.path.isdir(f) else "📄 [קובץ]  "
        lines.append({"text": f"{prefix} {f}", "type": ""})
    return {"lines": lines}