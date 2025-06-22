import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("My First GUI")
window.geometry("300x150")

# Add a label
label = tk.Label(window, text="Hello, Ayush!", font=("Arial", 16))
label.pack(pady=20)

# Start the GUI loop
window.mainloop()