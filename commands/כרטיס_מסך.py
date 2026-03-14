import subprocess

def execute(args):
    try:
        # פקודת WMIC לשליפת שם כרטיס המסך
        res = subprocess.check_output('wmic path win32_VideoController get name', shell=True).decode('cp862', errors='ignore')
        lines = res.splitlines()
        
        # ניקוי הפלט (דילוג על הכותרת ושורות ריקות)
        gpu_name = next((l.strip() for l in lines[1:] if l.strip()), "לא נמצא")
        
        return {
            "lines": [
                {"text": "🎮 כרטיס מסך זוהה במערכת:", "type": "success"},
                {"text": f"  דגם: {gpu_name}", "type": ""}
            ]
        }
    except Exception as e:
        return {"lines": [{"text": f"❌ שגיאה בשליפת נתוני כרטיס מסך: {e}", "type": "error"}]}