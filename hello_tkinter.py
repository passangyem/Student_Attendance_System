import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Hello World - Tkinter")
root.geometry("400x250")

# Create a label
label = tk.Label(
    root,
    text="Hello World!",
    font=("Arial", 20)
)
label.pack(pady=80)

# Run the application
root.mainloop()