import subprocess
import platform
import re

def execute(args):
    lines = []

    if platform.system() != "Windows":
        lines.append({"text": "❌ שגיאה: פקודה זו נתמכת כרגע רק במערכת הפעלה Windows.", "type": "error"})
        lines.append({"text": "למערכות אחרות יש להשתמש בפקודות כמו 'getent passwd' או 'cat /etc/passwd'.", "type": "sys-out"})
        return {"lines": lines}

    lines.append({"text": "👥 אוסף מידע על משתמשים מקומיים...", "type": "sys-out"})

    try:
        command = ["net", "user"]
        process = subprocess.run(command, capture_output=True, text=True, check=True, encoding='cp862') # cp862 for Hebrew in console
        output = process.stdout.strip()

        user_list_start = False
        user_names = []
        for line in output.splitlines():
            if "-------------------------------------------------------------------------------" in line:
                if user_list_start: # End of list
                    break
                user_list_start = True
                continue
            
            if user_list_start:
                # User names are typically on lines after the dashes, separated by spaces
                # Example: Administrator      Guest          user1
                current_line_users = re.findall(r'(\S+)', line)
                user_names.extend(current_line_users)
        
        if user_names:
            lines.append({"text": "----------------------------------------------------", "type": "sys-out"})
            lines.append({"text": "שם משתמש", "type": "sys-out"})
            lines.append({"text": "----------------------------------------------------", "type": "sys-out"})
            for user in user_names:
                lines.append({"text": user, "type": ""})
            lines.append({"text": "----------------------------------------------------", "type": "sys-out"})
            lines.append({"text": f"✅ סך הכל {len(user_names)} משתמשים מקומיים נמצאו.", "type": "success"})
        else:
            lines.append({"text": "⚠️ לא נמצאו משתמשים מקומיים.", "type": "sys-out"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה 'net' לא נמצאה. ודא שהיא מותקנת ובנתיב המערכת.", "type": "error"})
    except subprocess.CalledProcessError as cpe:
        lines.append({"text": f"❌ שגיאה בהפעלת 'net user': {cpe.stderr}", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
