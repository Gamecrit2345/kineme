import tkinter as tk
from tkinter import messagebox, filedialog
import random
import threading
import time

# ====================== POP-UP ADS ======================
ADS = [
    "🔥 Support the Dev! Star this repo ⭐",
    "💰 Gusto mo ng custom antivirus? PM me!",
    "🛡️ Kineme Antivirus - Educational Tool Only",
    "❤️ Like & Share para mas maraming ganito!",
    "🚀 Python Projects Available - Hire me!",
    "⚠️ This is just a simulation for learning",
    "📢 Follow @Gamecrit2345 on GitHub"
]

def show_random_ad():
    ad = random.choice(ADS)
    messagebox.showinfo("📢 Kineme Ads", ad)

# ====================== MAIN GUI ======================
class KinemeAntivirus:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🛡️ Kineme Antivirus")
        self.root.geometry("700x500")
        self.root.configure(bg="#0a0a0a")

        tk.Label(self.root, text="🛡️ Kineme Antivirus", 
                 font=("Arial", 20, "bold"), fg="#00ff00", bg="#0a0a0a").pack(pady=20)

        tk.Button(self.root, text="Scan Folder", command=self.scan_folder, 
                  bg="#0066ff", fg="white", font=("Arial", 12), width=20).pack(pady=10)
        
        tk.Button(self.root, text="Scan File", command=self.scan_file, 
                  bg="#0066ff", fg="white", font=("Arial", 12), width=20).pack(pady=10)

        self.log = tk.Text(self.root, height=15, bg="#111", fg="#0f0", font=("Consolas", 10))
        self.log.pack(padx=20, pady=20, fill="both", expand=True)

        # Auto pop-up ads every 25-40 seconds
        threading.Thread(target=self.ad_loop, daemon=True).start()

    def log_message(self, msg):
        self.log.insert(tk.END, f"[+] {msg}\n")
        self.log.see(tk.END)

    def ad_loop(self):
        while True:
            time.sleep(random.randint(25, 40))  # Random timing
            try:
                self.root.after(0, show_random_ad)
            except:
                break

    def scan_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.log_message(f"Scanning folder: {folder}")
            self.log_message("✅ Scan Complete (Simulation)")
            # Random ad after scan
            self.root.after(1500, show_random_ad)

    def scan_file(self):
        file = filedialog.askopenfilename()
        if file:
            self.log_message(f"Scanning file: {file}")
            self.log_message("✅ File is Clean (Simulation)")
            self.root.after(1200, show_random_ad)

if __name__ == "__main__":
    app = KinemeAntivirus()
    app.root.mainloop()
