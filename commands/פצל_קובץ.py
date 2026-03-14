import os

def execute(args):
    lines = []
    
    if len(args) < 3:
        lines.append({"text": "❌ שגיאה: יש לספק נתיב קובץ, גודל פיצול בבתים (לדוגמה: 1048576 עבור 1MB) ותבנית לשמות קבצי הפלט.", "type": "error"})
        lines.append({"text": "דוגמה: פצל_קובץ large_file.txt 1048576 output_part_", "type": "sys-out"})
        return {"lines": lines}

    input_file_path = args[0]
    try:
        chunk_size = int(args[1])
    except ValueError:
        lines.append({"text": "❌ שגיאה: גודל הפיצול חייב להיות מספר שלם.", "type": "error"})
        return {"lines": lines}
    output_prefix = args[2]

    if not os.path.exists(input_file_path):
        lines.append({"text": f"❌ שגיאה: קובץ הקלט '{input_file_path}' לא נמצא.", "type": "error"})
        return {"lines": lines}
    if not os.path.isfile(input_file_path):
        lines.append({"text": f"❌ שגיאה: '{input_file_path}' אינו קובץ.", "type": "error"})
        return {"lines": lines}
    if chunk_size <= 0:
        lines.append({"text": "❌ שגיאה: גודל הפיצול חייב להיות גדול מ-0.", "type": "error"})
        return {"lines": lines}

    lines.append({"text": f"✂️ מפצל את הקובץ '{input_file_path}' לחלקים בגודל {chunk_size} בתים...", "type": "sys-out"})

    try:
        part_num = 0
        with open(input_file_path, 'rb') as infile:
            while True:
                chunk = infile.read(chunk_size)
                if not chunk:
                    break # End of file
                
                part_num += 1
                output_file_path = f"{output_prefix}{part_num:03d}" # e.g., output_part_001
                
                with open(output_file_path, 'wb') as outfile:
                    outfile.write(chunk)
                lines.append({"text": f"  ✅ נוצר חלק: '{output_file_path}'", "type": ""})
        
        lines.append({"text": f"✅ פיצול קובץ הושלם. נוצרו {part_num} חלקים.", "type": "success"})

    except PermissionError:
        lines.append({"text": "❌ אין הרשאה לקרוא קובץ קלט או לכתוב קבצי פלט.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
