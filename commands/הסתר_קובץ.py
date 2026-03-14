import subprocess
import platform
import os

def execute(args):
    lines = []
    
    if len(args) < 2:
        lines.append({"text": "❌ שגיאה: יש לספק פעולה (הסתר/הצג) ונתיב לקובץ/תיקייה.", "type": "error"})
        lines.append({"text": "דוגמה: הסתר_קובץ הסתר my_secret_file.txt", "type": "sys-out"})
        lines.append({"text": "דוגמה: הסתר_קובץ הצג my_hidden_folder", "type": "sys-out"})
        return {"lines": lines}

    action = args[0].lower()
    target_path = args[1]

    if not os.path.exists(target_path):
        lines.append({"text": f"❌ שגיאה: הנתיב '{target_path}' לא נמצא.", "type": "error"})
        return {"lines": lines}

    if platform.system() == "Windows":
        attrib_param = "+H" if action == "הסתר" else "-H"
        command = ["attrib", attrib_param, target_path]
        
        lines.append({"text": f"⚙️ מנסה {action} את הנתיב '{target_path}'...", "type": "sys-out"})

        try:
            process = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8')
            output = process.stdout.strip()
            
            lines.append({"text": f"✅ הנתיב '{target_path}' {action} בהצלחה.", "type": "success"})
            if output:
                lines.append({"text": output, "type": "sys-out"})

        except FileNotFoundError:
            lines.append({"text": "❌ שגיאה: הפקודה 'attrib' לא נמצאה. ודא שהיא קיימת בנתיב המערכת.", "type": "error"})
        except subprocess.CalledProcessError as cpe:
            lines.append({"text": f"❌ שגיאה בהפעלת attrib: {cpe.stderr}", "type": "error"})
        except Exception as e:
            lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    else:
        lines.append({"text": "❌ שגיאה: פקודה זו נתמכת כרגע רק במערכת הפעלה Windows.", "type": "error"})
        lines.append({"text": "  במערכות דמויות יוניקס, קבצים ותיקיות מוסתרים על ידי קידומת נקודה (לדוגמה: .my_hidden_file).", "type": "sys-out"})
    
    return {"lines": lines}
