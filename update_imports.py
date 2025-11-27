import os
import glob

# Update all route files
route_files = glob.glob('routes/*.py')
for file_path in route_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the import
    content = content.replace('from app import db', 'from extensions import db')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {file_path}")

print("\nAll route files updated successfully!")
