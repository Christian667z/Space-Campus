import os
from pathlib import Path

def convert_md_to_py(directory):
    md_files = list(Path(directory).rglob('*.md'))
    for md_file in md_files:
        content = md_file.read_text(encoding='utf-8', errors='replace')
        # Escape triple quotes if any
        content = content.replace('\"\"\"', '\\\"\\\"\\\"')
        py_content = f'CONTENT = \"\"\"\\n{content}\\n\"\"\"\\n'
        
        py_file = md_file.with_suffix('.py')
        py_file.write_text(py_content, encoding='utf-8')
        md_file.unlink() # Delete the original md file
        print(f"Converted {md_file.name} to {py_file.name}")

if __name__ == '__main__':
    convert_md_to_py('c:/Users/DELL/Space-Dev/AstaAcademie/hacking')
