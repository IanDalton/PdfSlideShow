import tkinter as tk
 
window = tk.Tk()
window.title("Grid Manager")
 
#obteniendo resolucion del display
from screeninfo import get_monitors
def get_largest_screen():
    dmax = None
    h,w=0,0
    for m in get_monitors():
        if h*w < m.height*m.width:
            h,w=m.height,m.width
            dmax=m
    return h,w


window.attributes('-fullscreen',True)

for x in range(4):
   for y in range(3):
       frame = tk.Frame(
           master=window,
           relief=tk.RAISED,
           borderwidth=0,
           background="red"
       )
       #frame.config(bg="red")
       frame.grid(row=y, column=x)  # line 13
       t = tk.PhotoImage(file=f"ca{x+y}.jpg")
       print(f"ca{x+y}.jpg")
       label = tk.Label(master=frame,image=t)
       label.image = t
       label.pack()
       
window.mainloop()