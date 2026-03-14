import os
def execute(args):
    if len(args) < 2: return {"lines": [{"text": "שגיאה: הקלד 'שנה_שם [ישן] [חדש]'", "type": "error"}]}
    try:
        os.rename(args[0], args[1])
        return {"lines": [{"text": f"השם שונה בהצלחה ל-{args[1]}", "type": "success"}]}
    except Exception as e: return {"lines": [{"text": f"שגיאה: {e}", "type": "error"}]}