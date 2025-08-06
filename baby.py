import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage, messagebox
import json

class StoryApp:
    def __init__(self):
        self.window_width = 800
        self.window_height = 600
        self.current_scene = "first_touch"
        self.story_data = None
        
        self.setup_window()
        self.load_story()
        self.show_scene()
    
    def setup_window(self):
        """Configura la ventana principal"""
        self.window = tk.Tk()
        
        try:
            icon = PhotoImage(file='image.png')
            self.window.iconphoto(True, icon)
        except:
            print("No se encontró el icono, usando predeterminado")
        
        self.window.title('Nuestra Historia Interactiva 💕')
        self.window.configure(bg='#FFE4E1')  # Color de fondo rosa claro
        
        # Centrar ventana
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        center_x = int(screen_width/2 - self.window_width / 2)
        center_y = int(screen_height/2 - self.window_height / 2)
        
        self.window.geometry(f'{self.window_width}x{self.window_height}+{center_x}+{center_y}')
        self.window.resizable(True, True)
        
        # Frame principal con scroll
        self.main_frame = ttk.Frame(self.window, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas y scrollbar
        self.canvas = tk.Canvas(self.main_frame)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
    
    def load_story(self):
        """Carga la historia desde el archivo JSON"""
        try:
            with open('stories.json', 'r', encoding='utf-8') as f:
                self.story_data = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo stories.json")
            self.window.destroy()
        except json.JSONDecodeError:
            messagebox.showerror("Error", "El archivo JSON tiene errores de formato")
            self.window.destroy()
    
    def show_scene(self):
        """Muestra la escena actual y sus opciones"""
        # Limpiar frame anterior
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.story_data:
            return
            
        scene = self.story_data["scenes"].get(self.current_scene, None)
        
        if not scene:
            messagebox.showerror("Error", f"Escena '{self.current_scene}' no encontrada")
            return
        
        # Mostrar texto de la escena
        text_label = ttk.Label(
            self.scrollable_frame,
            text=scene["text"],
            wraplength=self.window_width - 50,
            font=('Helvetica', 12),
            justify="left"
        )
        text_label.pack(pady=10, padx=10, anchor="w")
        
        # Mostrar ending si existe
        if "ending" in scene:
            ending_label = ttk.Label(
                self.scrollable_frame,
                text=f"\n{scene['ending']}",
                wraplength=self.window_width - 50,
                font=('Helvetica', 12, 'italic'),
                foreground="blue",
                justify="left"
            )
            ending_label.pack(pady=5, padx=10, anchor="w")
        
        # Mostrar opciones si existen
        if "choices" in scene:
            choices_label = ttk.Label(
                self.scrollable_frame,
                text="\n¿Qué harás?",
                font=('Helvetica', 12, 'bold')
            )
            choices_label.pack(pady=10, anchor="w")
            
            for choice in scene["choices"]:
                choice_btn = ttk.Button(
                    self.scrollable_frame,
                    text=choice["text"],
                    command=lambda next_scene=choice["next_scene"]: self.make_choice(next_scene),
                    style='Accent.TButton'
                )
                choice_btn.pack(pady=5, fill=tk.X)
        else:
            # Si no hay opciones, mostrar botón para reiniciar
            restart_btn = ttk.Button(
                self.scrollable_frame,
                text="Volver al inicio",
                command=lambda: self.make_choice("first_touch"),
                style='Accent.TButton'
            )
            restart_btn.pack(pady=20)
    
    def make_choice(self, next_scene):
        """Maneja la selección de una opción"""
        self.current_scene = next_scene
        self.show_scene()
        # Auto-scroll al inicio
        self.canvas.yview_moveto(0)
    
    def run(self):
        """Ejecuta la aplicación"""
        # Configurar estilo
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Helvetica', 11), foreground='#8B008B')
        
        self.window.mainloop()

def main():
    app = StoryApp()
    app.run()

if __name__ == "__main__":
    main()