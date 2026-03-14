import os

def execute(args):
    lines = []
    
    if len(args) < 4:
        lines.append({"text": "❌ שגיאה: יש לספק פעולה (encrypt/decrypt), נתיב קובץ קלט, נתיב קובץ פלט ומפתח.", "type": "error"})
        lines.append({"text": "דוגמה: הצפנה_קובץ encrypt my_file.txt my_file.enc 'מפתח'", "type": "sys-out"})
        return {"lines": lines}

    action = args[0].lower()
    input_file = args[1]
    output_file = args[2]
    key = args[3]

    if not os.path.exists(input_file):
        lines.append({"text": f"❌ שגיאה: קובץ הקלט '{input_file}' לא נמצא.", "type": "error"})
        return {"lines": lines}
    if not os.path.isfile(input_file):
        lines.append({"text": f"❌ שגיאה: '{input_file}' אינו קובץ.", "type": "error"})
        return {"lines": lines}
    if not key:
        lines.append({"text": "❌ שגיאה: מפתח ההצפנה אינו יכול להיות ריק.", "type": "error"})
        return {"lines": lines}

    lines.append({"text": f"🔐 מבצע {action} של הקובץ '{input_file}'...", "type": "sys-out"})

    try:
        with open(input_file, 'rb') as fin, open(output_file, 'wb') as fout:
            key_bytes = key.encode('utf-8')
            key_len = len(key_bytes)
            
            i = 0
            while True:
                byte_read = fin.read(1)
                if not byte_read:
                    break # EOF
                
                xor_result = byte_read[0] ^ key_bytes[i % key_len]
                fout.write(bytes([xor_result]))
                i += 1
        
        lines.append({"text": f"✅ הקובץ {action} בהצלחה ונשמר כ-'{output_file}'.", "type": "success"})
        lines.append({"text": "⚠️ אזהרה: זוהי הצפנה פשוטה מאוד ואינה מאובטחת לשימוש אמיתי.", "type": "sys-out"})

    except PermissionError:
        lines.append({"text": "❌ אין הרשאה לקרוא קובץ קלט או לכתוב קובץ פלט.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
