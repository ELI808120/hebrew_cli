import os

def execute(args):
    lines = []
    
    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק שם קובץ.", "type": "error"})
        lines.append({"text": "דוגמה: צור_קובץ test.txt", "type": "sys-out"})
        return {"lines": lines}

    # לקיחת שם הקובץ (הפרמטר הראשון)
    file_path = args[0]
    
    # חיבור כל שאר המילים לתוכן אחד (מטפל ברווחים גם בלי מרכאות!)
    content_to_write = " ".join(args[1:]) if len(args) > 1 else ""

    lines.append({"text": f"✍️ יוצר קובץ '{file_path}'...", "type": "sys-out"})

    try:
        # טיפול בנתיבים ותיקיות
        dir_name = os.path.dirname(file_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
            lines.append({"text": f"ℹ️ נוצרה תיקייה: '{dir_name}'.", "type": "sys-out"})

        # כתיבה לקובץ
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content_to_write)
        
        if content_to_write:
            lines.append({"text": f"✅ הקובץ '{file_path}' נוצר עם התוכן.", "type": "success"})
        else:
            lines.append({"text": f"✅ הקובץ הריק '{file_path}' נוצר בהצלחה.", "type": "success"})

    except PermissionError:
        lines.append({"text": f"❌ אין הרשאה ליצור קובץ בנתיב הזה.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאה: {str(e)}", "type": "error"} )
    
    return {"lines": lines}