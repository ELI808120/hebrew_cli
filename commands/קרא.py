import os
def execute(args):
    if not args: return {"lines": [{"text": "שגיאה: ציין שם קובץ לקריאה", "type": "error"}]}
    try:
        with open(" ".join(args), 'r', encoding='utf-8') as f:
            return {"lines": [{"text": f"--- תוכן הקובץ ---\n{f.read()}", "type": ""}]}
    except Exception as e: return {"lines": [{"text": f"שגיאה: {e}", "type": "error"}]}