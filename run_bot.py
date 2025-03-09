import subprocess
import time
import sys
import os

# Virtual muhitga yo‘l qo'shish
venv_python = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe") if sys.platform == "win32" else os.path.join(os.getcwd(), "venv", "bin", "python")

while True:
    print("🔄 Bot ishga tushirilmoqda...")
    process = subprocess.Popen([venv_python, "main.py"])  # ✅ `main.py` ni to‘g‘ri Python bilan ishga tushirish
    process.wait()  # Bot to'xtashini kutish

    print("⚠️ Bot to'xtadi! 5 soniyadan keyin qayta ishga tushiriladi...")
    time.sleep(5)  # 5 soniya kutish va qayta ishga tushirish
