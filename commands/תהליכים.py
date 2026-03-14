import subprocess
import re

def execute(args):
    search_term = args[0].lower() if args else None
    lines = [{"text": "⚙️ סורק תהליכים פעילים במערכת...", "type": "sys-out"}]
    
    try:
        # הרצת tasklist
        res = subprocess.check_output("tasklist", shell=True, stderr=subprocess.STDOUT)
        try:
            output = res.decode('cp862', errors='ignore')
        except UnicodeDecodeError:
            output = res.decode('utf-8', errors='ignore')
            
        process_list = []
        
        # דילוג על שורות הכותרת המיותרות של ווינדוס
        for line in output.splitlines()[3:]:
            if not line.strip(): continue
            
            # פירוק השורה לנתונים לפי רווחים כפולים של ווינדוס
            match = re.match(r'^(.+?)\s+(\d+)\s+(.+?)\s+(\d+)\s+([\d,]+\s+[KMG])', line)
            if match:
                name = match.group(1).strip()
                pid = match.group(2).strip()
                mem = match.group(5).strip()
                
                # מנגנון החיפוש
                if search_term and search_term not in name.lower():
                    continue
                    
                process_list.append({"name": name, "pid": pid, "mem": mem})
        
        if not process_list:
            if search_term:
                return {"lines": [{"text": f"❌ לא נמצא תהליך בשם '{search_term}'.", "type": "error"}]}
            return {"lines": [{"text": "❌ לא נמצאו תהליכים.", "type": "error"}]}
            
        lines.append({"text": f"✅ נמצאו {len(process_list)} תהליכים תואמים:", "type": "success"})
        
        # בניית הרשימה
        for p in process_list[:15]:
            lines.append({"text": f"📌 מזהה: {p['pid']} | זיכרון: {p['mem']} | שם: {p['name']}", "type": ""})
            
        # אם יש יותר מ-15, נסתיר כדי לא להציף את המסך
        if len(process_list) > 15:
            lines.append({"text": f"... ועוד {len(process_list) - 15} תהליכים מוסתרים.", "type": "sys-out"})
            if not search_term:
                lines.append({"text": "💡 טיפ: הקלד 'תהליכים [שם]' כדי לחפש תהליך ספציפי (למשל: תהליכים chrome).", "type": "success"})
                
        return {"lines": lines}
        
    except Exception as e:
        return {"lines": [{"text": f"שגיאה בשליפת תהליכים: {e}", "type": "error"}]}