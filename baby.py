import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage, messagebox
import json
import random
import sys
import os

# pyinstaller --onefile --windowed --add-data "recursos;recursos" baby.py 
#               un archivo sin consola agregar cada archivos;destino 

class StoryApp:
    def __init__(self):

        
        self.window_width =700
        self.window_height = 500
        self.current_scene = "first_touch"
        self.story_data = None
        self.chapter_name = "First Touch"
        self.no_choice_but_next_scene = False
        self.index = -1

        self.load_phrases()
        self.setup_window()
        self.load_story()
        self.show_scene()
    
    
    def resource_path(self, relative_path):
        """ Obtener ruta absoluta al recurso, para PyInstaller """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def setup_window(self):
        """Configura la ventana principal"""
        self.window = tk.Tk()
        
        try:
            route = self.resource_path('recursos/heart.png')
            icon = PhotoImage(file=route)
            self.window.iconphoto(True, icon)
        except:
            print("No se encontró el icono, usando predeterminado")
        
        self.window.title('For you 💕')
        self.window.configure(bg="#c108ff")  # Color de fondo rosa claro
        
        # Centrar ventana
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        center_x = int(screen_width/2 - self.window_width / 2)
        center_y = int(screen_height/2 - self.window_height / 2)
        
        self.window.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        self.window.resizable(True, True)
        
        # Frame principal
        self.main_frame = tk.Frame(self.window, padx=10, background="#c108ff")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
    
    def load_story(self):
        """Carga la historia desde el archivo JSON"""
        try:
            route = self.resource_path('recursos/stories.json')
            with open(route, 'r', encoding='utf-8') as f:
                self.story_data = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo stories.json")
            self.window.destroy()
        except json.JSONDecodeError:
            messagebox.showerror("Error", "El archivo JSON tiene errores de formato")
            self.window.destroy()
    
    def load_phrases(self):
        try:
            route = self.resource_path('recursos/phrases.json')
            with open(route, 'r', encoding='utf-8') as p:
                self.phrases = json.load(p)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo stories.json")
            self.window.destroy()
        except json.JSONDecodeError:
            messagebox.showerror("Error", "El archivo JSON tiene errores de formato")
            self.window.destroy()
    
    def show_scene(self):
        """Muestra la escena actual y sus opciones"""
        # Limpiar frame anterior
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        if not self.story_data:
            return
            
        scene = self.story_data["scenes"].get(self.current_scene, None)
        
        if not scene:
            messagebox.showerror("Error", f"Escena '{self.current_scene}' no encontrada")
            return
        
        if "ending" in scene:
                self.chapter_name = scene['ending']
         # Mostrar ending si existe
        if self.chapter_name != '':
            ending_label = ttk.Label(
                self.main_frame,
                text=f"Chapter : {self.chapter_name}",
                wraplength=self.window_width - 15,
                font=('Helvetica', 12, 'bold italic'),
                foreground="#FFEA00",
                justify="left",
                background="#c108ff"
            )
            ending_label.pack(pady=5, anchor="center")
        
        # Mostrar texto de la escena
        text_label = ttk.Label(
            self.main_frame,
            text=scene["text"],
            wraplength=self.window_width-20,
            font=('Helvetica', 12),
            background="#c108ff",
            justify="left",
            foreground='white'
        )
        text_label.pack(pady=(10))
        
        # Mostrar opciones si existen
        if "choices" in scene:
            choices_label = ttk.Label(
                self.main_frame,
                text="\nWhat do you do?",
                font=('Helvetica', 12, 'bold'),
                background="#c108ff",
                foreground='white'
            )
            choices_label.pack(anchor='w', pady=(0,20))
            
            for choice in scene["choices"]:
                choice_btn = ttk.Button(
                    self.main_frame,
                    text=choice["text"],
                    command=lambda next_scene=choice["next_scene"]: self.make_choice(next_scene),
                    style='My.TButton'
                )
                choice_btn.pack(pady=5, fill=tk.X)
        else:
            # Si no hay opciones, mostrar botón para reiniciar
            restart_btn = ttk.Button(
                self.main_frame,
                text="Back to the beginning",
                command=lambda: self.make_choice("first_touch"),
                style='My.TButton'
            )
            restart_btn.pack(pady=20, anchor='s')
            ending_label.destroy()
            self.chapter_name = "First Touch"

            if scene["next_scene"]:
                self.no_choice_but_next_scene = True
            else:
                self.no_choice_but_next_scene = False

        if self.index >= 0:
            phrase_label = ttk.Label(
                self.main_frame,
                text=self.phrase,
                font=('Helvetica', 11, 'bold'),
                background="#c108ff",
                justify="center",
                foreground='white'
            )
            phrase_label.pack(pady=([30,0]))

        phrase_btn = ttk.Button(
                    self.main_frame,
                    text="Press me..",
                    command=lambda: self.get_phrase(),
                    style='My.HiddenButton.TButton'
                )
        phrase_btn.pack(pady=([0,30]),side="bottom")

    def get_phrase(self):
        index = random.randint(1, len(self.phrases))
        self.index = index
        self.phrase = self.phrases[index]
        self.show_scene()
        
    def make_choice(self, next_scene):
        """Maneja la selección de una opción"""
        self.current_scene = next_scene
        self.show_scene()
    
    def run(self):
        " Inicia la aplicacion"
        # Crear un objeto Style
        style = ttk.Style()

        style.theme_use('clam')  # Un tema que permite cambios en background

        # Configurar un estilo personalizado para botones
        style.configure('My.TButton', 
                        font=('Helvetica', 11, 'bold italic'),
                        foreground='#8B008B',
                        background='white',
                        padding=10)  # Espaciado interno
        # Cambios cuando el mouse está encima (hover)
        style.map('Hover.TButton',
                background=[('active', "#E0E0E0D6")])  # Fondo púrpura oscuro en hover
        
        style.configure('My.HiddenButton.TButton',
                        font=('Helvetica', 11, 'bold'),
                        foreground = 'black',
                        background='#c108ff',
                        borderwidth=0,
                        highlightthickness=0
                       )
        style.map('My.HiddenButton.TButton',
                        background=[('active', "#c108ff")])  # Fondo púrpura oscuro en hover
        self.window.mainloop()

def main():
    app = StoryApp()
    app.run()

if __name__ == "__main__":
    main()