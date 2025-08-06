import tkinter as tk #Importa todo tkinter, lo llamas tk
from tkinter import ttk #Solo importa el submódulo ttk, sin sobrenombre o import tkinter.ttk as ttk
from tkinter import PhotoImage
import json

window_width = 500
window_height = 400

def windowSetting():
    # Crear ventana principal
    root = tk.Tk()
    icon = PhotoImage(file='image.png')
    
    root.title('For you 💕')
    root.iconphoto(True, icon)
    root.configure(bg='lightblue')
    # get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    # set the position of the window to the center of the screen
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.resizable(False, False)

    # Crear un frame con padding
    frame = ttk.Frame(root, padding=10)
    frame.grid()    
    
    # Ejecutar la ventana
    root.mainloop()

def read_json(root):
    # Open and load the JSON file
    with open('stories.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Print the content
    print(data)

def main():
    windowSetting()
    read_json()

main()
