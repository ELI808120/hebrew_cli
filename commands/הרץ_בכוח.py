def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק פקודה להרצה עם הרשאות מנהל.", "type": "error"})
        lines.append({"text": "דוגמה: הרץ_בכוח net user Administrator active:yes", "type": "sys-out"})
        return {"lines": lines}

    command_to_run = " ".join(args)

    lines.append({"text": f"⚠️ אזהרה: הפקודה '{command_to_run}' תנסה לרוץ עם הרשאות מנהל.", "type": "error"})
    lines.append({"text": "  פעולה זו דורשת לרוב אישור (UAC) ולא תמיד ניתנת לביצוע אוטומטית מתוך תוכניות.", "type": "sys-out"})
    lines.append({"text": "  לביצוע פקודות הדורשות הרשאות מנהל, מומלץ להריץ את ה-CLI עצמו כמנהל.", "type": "sys-out"})
    lines.append({"text": "  הפקודה לא תבוצע כעת דרך 'הרץ_בכוח' מטעמי אבטחה ומגבלות סביבת הריצה.", "type": "sys-out"})
    
    return {"lines": lines}
