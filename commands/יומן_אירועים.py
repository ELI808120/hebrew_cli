import subprocess

def execute(args):
    lines = [{"text": "📋 בודק שגיאות מערכת אחרונות מיומן האירועים...", "type": "sys-out"}]
    try:
        # שליפת 5 אירועי שגיאה אחרונים
        cmd = 'wevtutil qe System /c:5 /rd:true /f:text /q:"*[System[(Level=2)]]"'
        res = subprocess.check_output(cmd, shell=True).decode('cp862', errors='ignore')
        
        if not res.strip():
            lines.append({"text": "✅ לא נמצאו שגיאות קריטיות לאחרונה.", "type": "success"})
        else:
            for line in res.splitlines():
                if "Description:" in line or "Date:" in line:
                    lines.append({"text": f"  {line.strip()}", "type": ""})
                    
        return {"lines": lines}
    except Exception as e:
        return {"lines": [{"text": f"❌ שגיאה בגישה ליומן האירועים: {e}", "type": "error"}]}