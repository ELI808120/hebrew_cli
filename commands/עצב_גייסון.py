import json

def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק מחרוזת JSON לעיצוב.", "type": "error"})
        lines.append({"text": 'דוגמה: עצב_גייסון \'{"name":"John", "age":30}\'', "type": "sys-out"})
        return {"lines": lines}

    json_string = " ".join(args)
    
    lines.append({"text": "✨ מעצב מחרוזת JSON...", "type": "sys-out"})

    try:
        parsed_json = json.loads(json_string)
        pretty_json = json.dumps(parsed_json, indent=2, ensure_ascii=False)
        
        lines.append({"text": "--- JSON מעוצב ---", "type": "success"})
        for line in pretty_json.splitlines():
            lines.append({"text": line, "type": ""})
        lines.append({"text": "✅ עיצוב JSON הושלם.", "type": "success"})

    except json.JSONDecodeError as e:
        lines.append({"text": f"❌ שגיאה בניתוח JSON: המחרוזת אינה JSON תקין. {e}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
