def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק מחרוזת להפוך.", "type": "error"})
        lines.append({"text": "דוגמה: הפוך_מחרוזת 'שלום עולם'", "type": "sys-out"})
        return {"lines": lines}

    input_string = " ".join(args)
    reversed_string = input_string[::-1]

    lines.append({"text": f"↔️ המחרוזת המקורית: '{input_string}'", "type": "sys-out"})
    lines.append({"text": f"✅ המחרוזת ההפוכה: '{reversed_string}'", "type": "success"})
    
    return {"lines": lines}
