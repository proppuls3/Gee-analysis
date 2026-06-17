import os
import zipfile

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        # Exclude massive dependency folders to keep the zip small
        if any(exclude in root for exclude in ['node_modules', '.next', '__pycache__', 'venv', '.git']):
            continue
        for file in files:
            if file in ['gee_project.zip', 'zip_project.py']:
                continue
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, path)
            ziph.write(file_path, arcname)

if __name__ == '__main__':
    print("Zipping project files...")
    with zipfile.ZipFile('gee_project.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir('.', zipf)
    print("Successfully created gee_project.zip!")
