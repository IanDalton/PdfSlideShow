import tkinter as tk
 
window = tk.Tk()
window.title("Grid Manager")
 
for x in range(3):
   for y in range(3):
       frame = tk.Frame(
           master=window,
           relief=tk.RAISED,
           borderwidth=0
       )
       frame.grid(row=x, column=y)  # line 13
       t = tk.PhotoImage(file=f"ca{x+y}.jpg")
       print(f"ca{x+y}.jpg")
       label = tk.Label(master=frame,image=t)
       label.image = t
       label.pack()
window.mainloop()