import tkinter as tk
from tkinter import messagebox, filedialog
import random
import threading
import time

# ====================== ADS ======================
ADS = [
    "🔥 Star this repo para mas maraming updates! ⭐",
    "💰 Gusto mo ng sariling custom tool? PM me!",
    "🛡️ Kineme Antivirus - Educational Project Only",
    "❤️ Like & Share ang project na 'to!",
    "🚀 More Python & Cybersecurity tools coming!",
    "⚠️ This is a simulation for learning only",
    "📢 Support Gamecrit2345 on GitHub",
    "💡 Follow me for more projects!"
]

def show_ad():
    ad = random.choice(ADS)
    messagebox.showinfo("📢 Kineme Advertisement", ad)

class KinemeAntivirus:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🛡️ Kineme Antivirus")
        self.root.geometry("750x550")
        self.root.configure(bg="#0a0a0a")

        tk.Label(self.root, text="🛡️ Kineme Antivirus", 
                 font=("Arial", 22, "bold"), fg="#00ff41", bg="#0a0a0a").pack(pady=15)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#0a0a0a")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Scan Folder", command=self.scan_folder,
                  bg="#0066ff", fg="white", font=("Arial", 11), width=18).pack(side=tk.LEFT, padx=8)
        
        tk.Button(btn_frame, text="Scan File", command=self.scan_file,
                  bg="#0066ff", fg="white", font=("Arial", 11), width=18).pack(side=tk.LEFT, padx=8)
        
        tk.Button(btn_frame, text="Test Ad", command=show_ad,
                  bg="#ff8800", fg="white", font=("Arial", 11), width=15).pack(side=tk.LEFT, padx=8)

        self.log = tk.Text(self.root, height=18, bg="#111111", fg="#00ff41", font=("Consolas", 10))
        self.log.pack(padx=20, pady=15, fill="both", expand=True)

        self.log_message("✅ Kineme Antivirus Ready!")
        self.log_message("Click 'Test Ad' to check if pop-up works")

        # Start auto ads
        threading.Thread(target=self.auto_ads, daemon=True).start()

    def log_message(self, msg):
        self.log.insert(tk.END, f"[+] {msg}\n")
        self.log.see(tk.END)

    def auto_ads(self):
        time.sleep(8)  # First ad after 8 seconds
        while True:
            try:
                self.root.after(0, show_ad)
                time.sleep(random.randint(18, 35))   # Every 18-35 seconds
            except:
                break

    def scan_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.log_message(f"Scanning folder: {folder}")
            for i in range(3):
                self.log_message(f"Checking files... {i+1}/3")
                time.sleep(0.6)
            self.log_message("✅ Scan Complete (Simulation)")
            self.root.after(800, show_ad)

    def scan_file(self):
        file = filedialog.askopenfilename()
        if file:
            self.log_message(f"Scanning: {file}")
            self.log_message("✅ File is Clean (Simulation)")
            self.root.after(600, show_ad)

if __name__ == "__main__":
    app = KinemeAntivirus()
    app.root.mainloop()
