def execute(args):
    lines = []
    
    if len(args) < 2:
        lines.append({"text": "❌ שגיאה: יש לספק פעולה (to_unicode/from_unicode) וטקסט/מחרוזת.", "type": "error"})
        lines.append({"text": "דוגמה: המר_יוניקוד to_unicode 'שלום'", "type": "sys-out"})
        lines.append({"text": "דוגמה: המר_יוניקוד from_unicode '\u05e9\u05dc\u05d5\u05dd'", "type": "sys-out"})
        return {"lines": lines}

    action = args[0].lower()
    data = " ".join(args[1:])

    try:
        if action == "to_unicode":
            # Convert string to unicode escape sequence
            unicode_escaped = data.encode('unicode_escape').decode('utf-8')
            lines.append({"text": f"➡️ הופך את '{data}' לייצוג יוניקוד:", "type": "sys-out"})
            lines.append({"text": f"✅ תוצאה: '{unicode_escaped}'", "type": "success"})
        elif action == "from_unicode":
            # Convert unicode escape sequence back to string
            # This requires adding a 'b' prefix to treat it as bytes literal
            # and then decoding. Or, safer, using string.decode('unicode_escape')
            # The input will be a string like "\u05e9\u05dc\u05d5\u05dd"
            
            # Need to be careful with double backslashes if input is from command line
            # Python's literal_eval can handle this, but it's not standard module for this usage.
            # Simple decode will work if it's already properly escaped.
            decoded_string = data.encode('utf-8').decode('unicode_escape')
            lines.append({"text": f"⬅️ הופך את ייצוג היוניקוד '{data}' לטקסט:", "type": "sys-out"})
            lines.append({"text": f"✅ תוצאה: '{decoded_string}'", "type": "success"})
        else:
            lines.append({"text": "❌ שגיאה: פעולה לא חוקית. השתמש ב-'to_unicode' או 'from_unicode'.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
