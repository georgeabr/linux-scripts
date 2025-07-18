#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import subprocess
import re
import os
from PIL import Image, ImageDraw, ImageTk

class BatteryMonitorApp:
    def __init__(self, master):
        self.master = master
        master.title("Battery Monitor")
        master.geometry("350x200")
        master.resizable(False, False)

        # Draw 16×16 battery icon and set as window/taskbar icon
        icon_img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        draw = ImageDraw.Draw(icon_img)
        draw.rectangle([0, 4, 12, 12], outline="white", width=1)
        draw.rectangle([12, 6, 15, 10], fill="white")
        tk_icon = ImageTk.PhotoImage(icon_img)
        master.iconphoto(True, tk_icon)
        self._icon_ref = tk_icon  # prevent garbage collection

        # Dark theme styling with larger button font
        style = ttk.Style()
        style.theme_use('clam')
        master.config(bg='#2e2e2e')
        style.configure('TFrame', background='#2e2e2e')
        style.configure('TLabel',
                        font=('monospace', 12),
                        foreground='white',
                        background='#2e2e2e')
        style.configure('TButton',
                        font=('monospace', 14),
                        background='#4a4a4a',
                        foreground='white')
        style.map('TButton', background=[('active', '#6a6a6a')])

        # Main container
        frame = ttk.Frame(master, padding=20)
        frame.pack(fill='both', expand=True)
        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)

        # Status row (tighter vertical spacing)
        ttk.Label(frame, text="Status:") \
            .grid(row=0, column=0, sticky='w', pady=1)
        self.status_val = ttk.Label(frame, text="N/A", anchor='w')
        self.status_val.grid(row=0, column=1, sticky='w', pady=1)

        # Percentage row
        ttk.Label(frame, text="Percentage:") \
            .grid(row=1, column=0, sticky='w', pady=1)
        self.percent_val = ttk.Label(frame, text="N/A", anchor='w')
        self.percent_val.grid(row=1, column=1, sticky='w', pady=1)

        # Time remaining row
        ttk.Label(frame, text="Time Remaining:") \
            .grid(row=2, column=0, sticky='w', pady=1)
        self.time_val = ttk.Label(frame, text="N/A", anchor='w')
        self.time_val.grid(row=2, column=1, sticky='w', pady=1)

        # Exit button (lowered down with more top padding)
        ttk.Button(frame, text="Exit", command=master.destroy) \
            .grid(row=3, column=0, columnspan=2, pady=(20, 0), sticky='ew')

        # Kick off periodic updates
        self.update_battery_info()

    def get_battery_info(self):
        try:
            out = subprocess.run(
                ['upower', '-e'],
                capture_output=True, text=True, check=True
            )
            path = next((l for l in out.stdout.splitlines() if '/battery' in l), None)
            if not path:
                return None

            info = subprocess.run(
                ['upower', '-i', path],
                capture_output=True, text=True, check=True
            )
            data = {'status': 'N/A', 'percentage': 'N/A', 'time': 'N/A'}
            for line in info.stdout.splitlines():
                if 'state:' in line:
                    data['status'] = line.split(':', 1)[1].strip()
                elif 'percentage:' in line:
                    data['percentage'] = line.split(':', 1)[1].strip()
                elif 'time to empty:' in line:
                    data['time'] = line.split(':', 1)[1].strip()
                elif 'time to full:' in line and data['status'] == 'charging':
                    data['time'] = line.split(':', 1)[1].strip()
            return data

        except subprocess.CalledProcessError:
            return None

    def format_time(self, s):
        if s == 'N/A':
            return 'N/A'
        t = re.sub(r'\s*\(est\)', '', s)
        t = (t.replace('hours', '')
              .replace('hour', '')
              .replace('minutes', '')
              .replace('minute', '')
              .strip())
        try:
            v = float(t.split()[0])
            h = int(v)
            m = int((v - h) * 60)
            return f"{h}:{m:02d}"
        except:
            return 'N/A'

    def update_battery_info(self):
        b = self.get_battery_info()
        title = "Battery Monitor"

        if b:
            st = b['status'].replace('-', ' ').title()
            pc = b['percentage']
            tm = self.format_time(b['time'])

            self.status_val.config(text=st)
            self.percent_val.config(text=pc)
            self.time_val.config(text=tm)

            tt = tm if tm != 'N/A' else pc
            if b['status'] == 'discharging':
                title = f"↓ {tt}"
            elif b['status'] == 'charging':
                title = f"↑ {tt}"
            elif b['status'] == 'fully-charged':
                title = f"✓ {pc}"
            else:
                title = f"{st} {pc}"
        else:
            self.status_val.config(text="Error/No Battery")
            self.percent_val.config(text="N/A")
            self.time_val.config(text="N/A")
            title = "Battery Monitor (Error)"

        self.master.title(title)
        self.master.after(5000, self.update_battery_info)


if __name__ == "__main__":
    if not (os.path.exists('/usr/bin/upower') or os.path.exists('/bin/upower')):
        print("UPower not found. Install it to proceed.")
        exit(1)

    root = tk.Tk()
    app = BatteryMonitorApp(root)
    root.mainloop()

