import os

def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק נתיב לקובץ למיון.", "type": "error"})
        lines.append({"text": "דוגמה: סדר_קובץ my_list.txt", "type": "sys-out"})
        lines.append({"text": "דוגמה: סדר_קובץ my_list.txt output.txt (למיון ושמירה לקובץ חדש)", "type": "sys-out"})
        return {"lines": lines}

    input_file_path = args[0]
    output_file_path = None
    if len(args) > 1:
        output_file_path = args[1]

    if not os.path.exists(input_file_path):
        lines.append({"text": f"❌ שגיאה: קובץ הקלט '{input_file_path}' לא נמצא.", "type": "error"})
        return {"lines": lines}
    if not os.path.isfile(input_file_path):
        lines.append({"text": f"❌ שגיאה: '{input_file_path}' אינו קובץ.", "type": "error"})
        return {"lines": lines}

    lines.append({"text": f"📝 ממיין שורות בקובץ '{input_file_path}'...", "type": "sys-out"})

    try:
        with open(input_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            file_lines = f.readlines()
        
        # Strip whitespace and sort
        sorted_lines = sorted([line.strip() for line in file_lines if line.strip()])

        if output_file_path:
            with open(output_file_path, 'w', encoding='utf-8') as f:
                for line in sorted_lines:
                    f.write(line + '
')
            lines.append({"text": f"✅ השורות מוינו ונשמרו בהצלחה בקובץ '{output_file_path}'.", "type": "success"})
        else:
            lines.append({"text": "--- שורות ממוינות ---", "type": "success"})
            for line in sorted_lines:
                lines.append({"text": line, "type": ""})
            lines.append({"text": "✅ מיון הושלם.", "type": "success"})

    except PermissionError:
        lines.append({"text": f"❌ אין הרשאה לקרוא את קובץ הקלט או לכתוב לקובץ הפלט.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
