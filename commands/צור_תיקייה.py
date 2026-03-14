import os
def execute(args):
    if not args: return {"lines": [{"text": "שגיאה: ציין שם תיקייה", "type": "error"}]}
    try:
        os.mkdir(" ".join(args))
        return {"lines": [{"text": f"התיקייה '{' '.join(args)}' נוצרה בהצלחה", "type": "success"}]}
    except Exception as e: return {"lines": [{"text": f"שגיאה: {e}", "type": "error"}]}