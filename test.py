import tkinter as tk

def select(btn):
    def select_button():
        for other_btn in buttons:
            deactivate(other_btn)
        btn.config(bg='green', activebackground='green', relief=tk.SUNKEN)
    return select_button

def deactivate(btn):
    btn.config(bg='gray', activebackground='gray', relief=tk.RAISED)

list_ = ['A', 'B', 'C']
buttons = []

root = tk.Tk()

for i, name in enumerate(list_, 2):
    btn = tk.Button(root, text=name)
    btn['command'] = select(btn)
    btn.grid(row=i, column=0, sticky=tk.W)
    buttons.append(btn)

root.mainloop()
