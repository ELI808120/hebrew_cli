import subprocess
import platform

def execute(args):
    lines = []
    
    if platform.system() != "Windows":
        lines.append({"text": "❌ שגיאה: פקודה זו נתמכת כרגע רק במערכת הפעלה Windows (באמצעות Winget).", "type": "error"})
        return {"lines": lines}

    if not args:
        lines.append({"text": "❌ שגיאה: יש לספק את שם החבילה להתקנה.", "type": "error"})
        lines.append({"text": "דוגמה: התקן_תוכנה VLC", "type": "sys-out"})
        return {"lines": lines}

    package_name = args[0]
    
    lines.append({"text": f"📥 מנסה להתקין את '{package_name}' באמצעות Winget...", "type": "sys-out"})

    try:
        command = ["winget", "install", "--id", package_name, "--accept-source-agreements", "--accept-package-agreements"]
        process = subprocess.run(command, capture_output=True, text=True, check=False, encoding='utf-8')
        output = process.stdout.strip()
        stderr_output = process.stderr.strip()

        if process.returncode == 0:
            lines.append({"text": f"✅ התקנת '{package_name}' הושלמה בהצלחה.", "type": "success"})
        else:
            lines.append({"text": f"❌ התקנת '{package_name}' נכשלה. קוד יציאה: {process.returncode}.", "type": "error"})
            if output: lines.append({"text": output, "type": "sys-out"})
            if stderr_output: lines.append({"text": stderr_output, "type": "error"})

    except FileNotFoundError:
        lines.append({"text": "❌ שגיאה: הפקודה 'winget' לא נמצאה. ודא ש-Windows Package Manager מותקן ובנתיב המערכת.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
