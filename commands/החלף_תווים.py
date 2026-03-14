def execute(args):
    lines = []
    
    if len(args) < 3:
        lines.append({"text": "❌ שגיאה: יש לספק מחרוזת, תו להחלפה ותו חלופי.", "type": "error"})
        lines.append({"text": "דוגמה: החלף_תווים 'שלום עולם' ו ה", "type": "sys-out"})
        return {"lines": lines}

    input_string = args[0]
    char_to_replace = args[1]
    replacement_char = args[2]

    if len(char_to_replace) != 1 or len(replacement_char) != 1:
        lines.append({"text": "❌ שגיאה: 'תו להחלפה' ו-'תו חלופי' חייבים להיות תו בודד.", "type": "error"})
        return {"lines": lines}

    lines.append({"text": f"🔄 מחליף את התו '{char_to_replace}' ב-' בשלבי '{replacement_char}' במחרוזת '{input_string}'...", "type": "sys-out"})

    try:
        modified_string = input_string.replace(char_to_replace, replacement_char)
        lines.append({"text": f"✅ המחרוזת לאחר ההחלפה: '{modified_string}'", "type": "success"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
