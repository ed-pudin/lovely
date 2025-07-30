import tkinter as tk

def windowSetting():
    root = tk.Tk()
    root.title('Hi baby I love you so much')

    window_width = 500
    window_height = 400

    # get the screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    # set the position of the window to the center of the screen
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    root.resizable(False, False)


    root.mainloop()
windowSetting()
