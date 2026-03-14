import os

def execute(args):
    lines = []
    
    start_path = "." # Default to current directory
    if args:
        start_path = args[0]
        if not os.path.exists(start_path):
            lines.append({"text": f"❌ שגיאה: הנתיב '{start_path}' לא נמצא.", "type": "error"})
            return {"lines": lines}
        if not os.path.isdir(start_path):
            lines.append({"text": f"❌ שגיאה: '{start_path}' אינו תיקייה.", "type": "error"})
            return {"lines": lines}

    lines.append({"text": f"🌳 מציג מבנה עץ עבור '{start_path}'...", "type": "sys-out"})

    try:
        def generate_tree(current_path, indent=""):
            # Add current directory itself to the tree display
            lines.append({"text": f"{indent}📁 {os.path.basename(current_path)}/", "type": ""})
            
            # Get all entries (files and directories)
            entries = sorted(os.listdir(current_path))
            
            for i, entry in enumerate(entries):
                full_path = os.path.join(current_path, entry)
                is_last = (i == len(entries) - 1)
                
                # Determine connector based on whether it's the last entry
                connector = "└── " if is_last else "├── "
                next_indent = indent + ("    " if is_last else "│   ")

                if os.path.isdir(full_path):
                    # Recursive call for subdirectories
                    lines.append({"text": f"{indent}{connector}📁 {entry}", "type": ""})
                    generate_tree(full_path, next_indent)
                else:
                    lines.append({"text": f"{indent}{connector}📄 {entry}", "type": ""})

        # Start generating the tree from the base path
        # Special handling for the very first entry if it's the current dir
        if start_path == ".":
            lines.append({"text": "📁 ./", "type": ""})
            entries_at_root = sorted(os.listdir(start_path))
            for i, entry in enumerate(entries_at_root):
                full_path = os.path.join(start_path, entry)
                is_last = (i == len(entries_at_root) - 1)
                connector = "└── " if is_last else "├── "
                next_indent = "    " if is_last else "│   "

                if os.path.isdir(full_path):
                    lines.append({"text": f"{connector}📁 {entry}", "type": ""})
                    generate_tree(full_path, next_indent)
                else:
                    lines.append({"text": f"{connector}📄 {entry}", "type": ""})
        else:
            # For a specified directory, only list its contents recursively
            lines.append({"text": f"📁 {os.path.basename(start_path)}/", "type": ""})
            entries_at_root = sorted(os.listdir(start_path))
            for i, entry in enumerate(entries_at_root):
                full_path = os.path.join(start_path, entry)
                is_last = (i == len(entries_at_root) - 1)
                connector = "└── " if is_last else "├── "
                next_indent = "    " if is_last else "│   "

                if os.path.isdir(full_path):
                    lines.append({"text": f"{connector}📁 {entry}", "type": ""})
                    generate_tree(full_path, next_indent)
                else:
                    lines.append({"text": f"{connector}📄 {entry}", "type": ""})

        lines.append({"text": "✅ הצגת עץ תיקיות הושלמה.", "type": "success"})

    except PermissionError:
        lines.append({"text": f"❌ אין הרשאה לגשת לנתיב '{start_path}'.", "type": "error"})
    except Exception as e:
        lines.append({"text": f"❌ שגיאת מערכת בלתי צפויה: {e}", "type": "error"})
    
    return {"lines": lines}
