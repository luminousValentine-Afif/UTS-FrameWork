import os
import shutil
import subprocess
import colorama


color = colorama.Fore

def reset_db():
    for root, dirs, files in os.walk('.'):
        for dir in dirs:
            if dir == '__pycache__': shutil.rmtree(os.path.join(root, dir))

    if os.path.exists('db.sqlite3'): os.remove('db.sqlite3')

    migrations_dir = os.path.join('api', 'migrations')
    if os.path.isdir(migrations_dir):
        for file in os.listdir(migrations_dir):
            if file != '__init__.py': os.remove(os.path.join(migrations_dir, file))
                
    if subprocess.run(['python', 'manage.py', 'makemigrations']).returncode == 0: print(color.GREEN + "[+] Created migrations file successfully." + color.RESET)
    else: print(color.RED + "[-] Failed to created migrations file." + color.RESET)
        
    if subprocess.run(['python', 'manage.py', 'migrate']).returncode == 0: print(color.GREEN + "[+] Applied migrations successfully." + color.RESET)
    else: print(color.RED + "[-] Failed to applied migrations." + color.RESET)
    
    
if __name__ == '__main__':
    reset_db()