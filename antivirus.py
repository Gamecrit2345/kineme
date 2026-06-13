# antivirus.py
import os
import hashlib

# List of fake virus signatures (for simulation)
VIRUS_SIGNATURES = [
    "malicious_code",
    "virus_test",
    "trojan",
    "ransomware_sim",
    "keylogger"
]

def get_file_hash(file_path):
    """Kunin ang MD5 hash ng file"""
    try:
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def scan_file(file_path):
    """I-scan ang isang file"""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().lower()
            
        for signature in VIRUS_SIGNATURES:
            if signature in content:
                return True, f"Virus detected: {signature}"
                
        # Check file extension
        suspicious_ext = ['.exe', '.bat', '.scr', '.pif']
        if any(file_path.lower().endswith(ext) for ext in suspicious_ext):
            return True, "Suspicious file extension"
            
        return False, "Clean"
    except:
        return False, "Cannot read file"

def scan_directory(directory):
    """I-scan ang buong folder"""
    print(f"🔍 Scanning directory: {directory}\n")
    threats = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            infected, message = scan_file(file_path)
            
            if infected:
                print(f"🚨 THREAT FOUND: {file_path}")
                print(f"   Reason: {message}\n")
                threats += 1
            else:
                print(f"✅ Clean: {file}")
    
    print(f"\nScan Complete! Found {threats} threat(s).")

if __name__ == "__main__":
    print("🛡️ Simple Antivirus Simulator")
    target = input("Enter folder to scan (e.g. . or C:\\Test): ") or "."
    scan_directory(target)
