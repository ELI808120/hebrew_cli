import os

def execute(args):
    lines = []
    
    if len(args) < 2:
        lines.append({"text": "❌ שגיאה: יש לספק נתיב לקובץ פלט ונתיבים לקבצי קלט לצירוף.", "type": "error"})
        lines.append({"text": "דוגמה: שלב_קבצים combined.txt part_001 part_002", "type": "sys-out"})
        return {"lines": lines}

    output_file_path = args[0]
    input_files = args[1:]

    lines.append({"text": f"🔗 משלב קבצים לתוך '{output_file_path}'...", "type": "sys-out"})

    try:
        with open(output_file_path, 'wb') as outfile:
            for input_file_path in input_files:
                if not os.path.exists(input_file_path):
                    lines.append({"text": f"⚠️ קובץ קלט '{input_file_path}' לא נמצא. מדלג.", "type": "sys-out"})
                    continue
                if not os.path.isfile(input_file_path):
                    lines.append({"text": f"⚠️ '{input_file_path}' אינו קובץ. מדלג.", "type": "sys-out"})
                    continue

                lines.append({"text": f"  ✅ מוסיף את '{input_file_path}'...", "type": ""})
                with open(input_file_path, 'rb') as infile:
                    outfile.write(infile.read())
        
        lines.append({"text": f"✅ שילוב קבצים הושלם. קובץ פלט: '{output_file_path}'.", "type": "success"})

    except PermissionError:
        lines.append({"text": "❌ אין הרשאה לקרוא קבצי קלט או לכתוב קובץ פלט.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
