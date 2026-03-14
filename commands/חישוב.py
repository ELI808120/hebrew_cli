def execute(args):
    if not args: return {"lines": [{"text": "שגיאה: הזן תרגיל (למשל: חישוב 5 * 10)", "type": "error"}]}
    try:
        # שימוש ב-eval בטוח יחסית רק לחישובים
        expr = " ".join(args).replace("^", "**")
        result = eval(expr, {"__builtins__": None}, {})
        return {"lines": [{"text": f"תוצאה: {result}", "type": "success"}]}
    except Exception as e: return {"lines": [{"text": "שגיאה בתרגיל", "type": "error"}]}