import os

def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק נתיב לקובץ לספירה.", "type": "error"})
        lines.append({"text": "דוגמה: ספור_מילים my_document.txt", "type": "sys-out"})
        return {"lines": lines}

    file_path = args[0]

    if not os.path.exists(file_path):
        lines.append({"text": f"❌ שגיאה: הקובץ '{file_path}' לא נמצא.", "type": "error"})
        return {"lines": lines}
    if not os.path.isfile(file_path):
        lines.append({"text": f"❌ שגיאה: '{file_path}' אינו קובץ.", "type": "error"})
        return {"lines": lines}

    lines.append({"text": f"🔢 סופר מילים, שורות ותווים ב-'{file_path}'...", "type": "sys-out"})

    try:
        line_count = 0
        word_count = 0
        char_count = 0
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line_count += 1
                char_count += len(line)
                word_count += len(line.split())
        
        lines.append({"text": "--- סטטיסטיקות קובץ ---", "type": "success"})
        lines.append({"text": f"  שורות: {line_count}", "type": ""})
        lines.append({"text": f"  מילים: {word_count}", "type": ""})
        lines.append({"text": f"  תווים: {char_count}", "type": ""})
        lines.append({"text": "------------------------", "type": "sys-out"})
        lines.append({"text": "✅ ספירה הושלמה.", "type": "success"})

    except PermissionError:
        lines.append({"text": f"❌ אין הרשאה לקרוא את הקובץ '{file_path}'.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאה בקריאת הקובץ '{file_path}': {e}", "type": "error"})
    
    return {"lines": lines}
