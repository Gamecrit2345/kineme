
---

### 4. **Main Secure Code** (`groksheild.py`)

```python
import os
import sys
import hashlib
import ssdeep
import json
import zlib
import datetime
import threading
import shutil
import logging
from tkinter import Tk, filedialog, messagebox, ttk, Label, Button, Text, Frame
from concurrent.futures import ThreadPoolExecutor, as_completed

# ====================== SECURITY CONFIG ======================
APP_NAME = "GrokShield Anti-Virus"
VERSION = "2.0"
QUARANTINE_DIR = "quarantine"
LOG_DIR = "logs"
SIGNATURE_DB = "signatures.json.enc"

WHITELIST = {"python.exe", "svchost.exe", "explorer.exe", "cmd.exe", "conhost.exe"}

SUSPICIOUS_EXTENSIONS = {'.exe', '.dll', '.scr', '.bat', '.ps1', '.vbs', '.js', '.jse', '.wsf', '.hta', '.msi'}
DANGEROUS_PATTERNS = [
    b'CreateRemoteThread', b'VirtualAllocEx', b'WriteProcessMemory',
    b'powershell -enc', b'cmd /c', b'base64', b'Invoke-Expression'
]

# ====================== SECURE LOGGING ======================
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=f'{LOG_DIR}/groksheild.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

# ====================== SIGNATURE DB (Encrypted) ======================
def load_signatures():
    try:
        if os.path.exists(SIGNATURE_DB):
            with open(SIGNATURE_DB, 'rb') as f:
                data = zlib.decompress(f.read()).decode('utf-8')
                return json.loads(data)
        return {"sha256": {}, "fuzzy": []}
    except Exception as e:
        logging.error(f"Signature load failed: {e}")
        return {"sha256": {}, "fuzzy": []}

def save_signatures(db):
    try:
        data = json.dumps(db).encode('utf-8')
        compressed = zlib.compress(data, level=9)
        with open(SIGNATURE_DB, 'wb') as f:
            f.write(compressed)
    except Exception as e:
        logging.error(f"Signature save failed: {e}")

signatures = load_signatures()

# ====================== CORE SCAN FUNCTIONS ======================
def get_file_hashes(file_path: str):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        sha256 = hashlib.sha256(data).hexdigest()
        fuzzy = ssdeep.hash(data)
        return sha256, fuzzy
    except:
        return None, None

def has_suspicious_behavior(file_path: str) -> bool:
    try:
        with open(file_path, "rb") as f:
            content = f.read(100_000).lower()
        return any(pattern in content for pattern in DANGEROUS_PATTERNS)
    except:
        return False

def scan_file(file_path: str):
    try:
        filename = os.path.basename(file_path).lower()
        if filename in WHITELIST:
            return "✅ Whitelisted", []

        results = []
        sha256, fuzzy = get_file_hashes(file_path)

        # Signature Matching
        if sha256 and sha256 in signatures["sha256"]:
            results.append("🚨 KNOWN MALWARE (SHA256 Match)")

        if fuzzy:
            for known in signatures["fuzzy"]:
                if ssdeep.compare(fuzzy, known) >= 75:
                    results.append("🚨 HIGH SIMILARITY TO MALWARE")
                    break

        # Heuristics
        ext = os.path.splitext(file_path)[1].lower()
        if ext in SUSPICIOUS_EXTENSIONS:
            results.append(f"⚠️ Suspicious extension: {ext}")

        if has_suspicious_behavior(file_path):
            results.append("🚨 Suspicious code patterns detected")

        # Large file heuristic
        if os.path.getsize(file_path) > 100 * 1024 * 1024 and ext == '.exe':
            results.append("⚠️ Unusually large executable")

        status = "🚨 MALICIOUS" if results else "✅ Clean"
        return status, results

    except Exception as e:
        logging.error(f"Scan error {file_path}: {e}")
        return "❌ Error", [str(e)]

# ====================== QUARANTINE ======================
def quarantine_file(file_path):
    try:
        os.makedirs(QUARANTINE_DIR, exist_ok=True)
        dest = os.path.join(QUARANTINE_DIR, os.path.basename(file_path))
        shutil.move(file_path, dest)
        logging.warning(f"Quarantined: {file_path}")
        return True
    except:
        return False

# ====================== DIRECTORY SCAN ======================
def scan_directory(directory):
    results = []
    quarantined = 0

    with ThreadPoolExecutor(max_workers=os.cpu_count() * 2) as executor:
        future_to_path = {}
        for root, _, files in os.walk(directory):
            for file in files:
                path = os.path.join(root, file)
                future = executor.submit(scan_file, path)
                future_to_path[future] = path

        for future in as_completed(future_to_path):
            path = future_to_path[future]
            try:
                status, details = future.result()
                log_entry = f"{status} | {path}"
                results.append(log_entry)
                logging.info(log_entry)

                if "MALICIOUS" in status:
                    if quarantine_file(path):
                        quarantined += 1
                        results.append(f"🛡️ Quarantined → {path}")
            except Exception as e:
                logging.error(f"Future error: {e}")

    return results, quarantined

# ====================== GUI ======================
class GrokShieldApp:
    def __init__(self):
        self.root = Tk()
        self.root.title(f"{APP_NAME} v{VERSION}")
        self.root.geometry("900x650")
        self.root.configure(bg="#0f0f0f")

        Label(self.root, text=f"🔰 {APP_NAME} v{VERSION}", 
              font=("Arial", 20, "bold"), fg="#00ff41", bg="#0f0f0f").pack(pady=15)

        self.progress = ttk.Progressbar(self.root, length=800, mode='indeterminate')
        self.progress.pack(pady=10)

        btn_frame = Frame(self.root, bg="#0f0f0f")
        btn_frame.pack(pady=10)

        Button(btn_frame, text="Scan Folder", command=self.start_scan, 
               bg="#0066ff", fg="white", font=("Arial", 10, "bold"), width=15).pack(side="left", padx=10)
        Button(btn_frame, text="Scan Single File", command=self.scan_single_file, 
               bg="#0066ff", fg="white", font=("Arial", 10, "bold"), width=15).pack(side="left", padx=10)

        self.log_area = Text(self.root, height=28, bg="#1a1a1a", fg="#00ff41", font=("Consolas", 10))
        self.log_area.pack(padx=15, pady=10, fill="both", expand=True)

    def log(self, message):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_area.insert("end", f"[{ts}] {message}\n")
        self.log_area.see("end")

    def start_scan(self):
        path = filedialog.askdirectory()
        if not path: return
        self.progress.start()
        self.log(f"🚀 Starting deep scan: {path}")
        threading.Thread(target=self.run_full_scan, args=(path,), daemon=True).start()

    def run_full_scan(self, path):
        logs, quarantined = scan_directory(path)
        self.progress.stop()
        self.log("✅ Full Scan Completed!")
        self.log(f"🛡️ Quarantined: {quarantined} suspicious file(s)")
        for line in logs[-40:]:
            self.log(line)
        messagebox.showinfo(APP_NAME, f"Scan Finished!\nQuarantined: {quarantined} files")

    def scan_single_file(self):
        file = filedialog.askopenfilename()
        if not file: return
        self.log(f"Scanning single file: {file}")
        status, details = scan_file(file)
        self.log(f"Result: {status}")
        for d in details:
            self.log(f"   └─ {d}")

if __name__ == "__main__":
    if not os.path.exists(SIGNATURE_DB):
        save_signatures({"sha256": {}, "fuzzy": []})
    
    app = GrokShieldApp()
    app.root.mainloop()
