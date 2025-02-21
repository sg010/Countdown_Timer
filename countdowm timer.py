import time
import threading
import os
import tkinter as tk
from tkinter import messagebox

# Function to clear the console screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Countdown function
def countdown_timer(seconds, label, root):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer_display = f"{mins:02}:{secs:02}"
        label.config(text=f"Time Left: {timer_display}")
        root.update()
        time.sleep(1)
        seconds -= 1
    
    label.config(text="Time's up! 🔔")
    notify_user()
    messagebox.showinfo("Countdown Timer", "Time's up!")

# Function to notify user when timer ends
def notify_user():
    try:
        # Windows Notification
        if os.name == 'nt':
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast("Countdown Timer", "Time's up!", duration=5)
        else:
            # Mac/Linux Notification
            os.system('notify-send "Countdown Timer" "Times up!"')
    except Exception as e:
        print("Notification error:", e)

def start_countdown(entry, label, root):
    try:
        duration = entry.get()
        if duration.lower().endswith('m'):
            seconds = int(duration[:-1]) * 60
        else:
            seconds = int(duration[:-1]) if duration.lower().endswith('s') else int(duration)
        
        # Start countdown in a separate thread
        timer_thread = threading.Thread(target=countdown_timer, args=(seconds, label, root))
        timer_thread.start()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter time in seconds (e.g., 120) or minutes (e.g., 2m).")

def main():
    root = tk.Tk()
    root.title("Countdown Timer")
    root.geometry("300x200")
    
    tk.Label(root, text="Enter time (e.g., 2m or 120s):").pack(pady=10)
    entry = tk.Entry(root)
    entry.pack(pady=5)
    
    label = tk.Label(root, text="Time Left: 00:00", font=("Helvetica", 14))
    label.pack(pady=10)
    
    start_button = tk.Button(root, text="Start Timer", command=lambda: start_countdown(entry, label, root))
    start_button.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
