import os
def execute(args):
    if not args: return {"lines": [{"text": "שגיאה: ציין שם קובץ למחיקה", "type": "error"}]}
    try:
        os.remove(" ".join(args))
        return {"lines": [{"text": "הקובץ נמחק בהצלחה", "type": "success"}]}
    except Exception as e: return {"lines": [{"text": f"שגיאה: {e}", "type": "error"}]}