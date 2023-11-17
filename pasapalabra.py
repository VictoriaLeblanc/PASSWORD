import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

class LoginVentana:
    def __init__(self, root):
        self.root = root
        self.root.title("Pass Word - Login")
        self.root.geometry("300x200")
        self.root.configure(bg="pink") 


        self.label_usuario = tk.Label(root, text="Usuario:",  bg="pink", fg="white")
        self.label_usuario.pack()

        self.entry_usuario = tk.Entry(root)
        self.entry_usuario.pack()

        self.label_contrasena = tk.Label(root, text="Contraseña:", bg="pink", fg="white")
        self.label_contrasena.pack()

        self.entry_contrasena = tk.Entry(root, show="*")
        self.entry_contrasena.pack()

        self.btn_login = tk.Button(root, text="Iniciar Sesión",   command=self.iniciar_sesion,  bg="white", fg="black")
        self.btn_login.pack()

    def iniciar_sesion(self):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        # verifica el ingreso
        if usuario == "usuario" and contrasena == "contrasena":
            self.root.destroy()
            app = PasapalabraApp()
        else:
            messagebox.showerror("Error de inicio de sesión", 
            "Credenciales incorrectas")

class PasapalabraApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pasapalabra")
        self.root.configure(bg="pink")

        # Inicia base de datos y la tabla de preguntas
        self.conn = sqlite3.connect('preguntas.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS preguntas (id 
        INTEGER PRIMARY KEY, letra TEXT, pregunta TEXT, respuesta 
        TEXT)''')

        # Cargar las preguntas desde la base de datos
        self.cargar_preguntas()

        # Inicializar variables
        self.pregunta_actual = None
        self.respuesta_usuario = tk.StringVar()

       
        self.label_pregunta = tk.Label(self.root, text="", font= 
        ("Arial", 12,))
        self.label_pregunta.pack()
        self.root.geometry("300x200")
        

        self.entry_respuesta = tk.Entry(self.root, 
        textvariable=self.respuesta_usuario)
        self.entry_respuesta.pack()

        self.btn_contestar = tk.Button(self.root, text="Contestar",command=self.verificar_respuesta, bg="white", fg="black")
        self.btn_contestar.pack()

        self.btn_pasapalabra = tk.Button(self.root,   text="Pasapalabra", command=self.siguiente_pregunta,bg="white", fg="black")
        self.btn_pasapalabra.pack()

        # Inicia juego
        self.iniciar_juego()

    def cargar_preguntas(self):
        # Consulta las preguntas desde la base de datos
        self.c.execute("SELECT * FROM preguntas")
        self.preguntas_respuestas = self.c.fetchall()

        
        if not self.preguntas_respuestas:
            preguntas_ejemplo = [
                ("A", "insecto de color amarillo con rayas negras", 
                "abeja"),
              ("B", "EL mejor equipo argentino de futbol", "Boca"),
              ("C", "Animal de uso para mortadela", "Caballo"),
              ("D", "Parte del cuerpo distal que tiene tres falanges ", 
              "Dedo"),
              ("E", "mamíferos placentarios del orden Proboscidea.", 
               "Elefante"), 
               ("F","deporte que los hombres creen jugar a la perfeccion.", "Futbol"),
               ("G", "Animal al cual identificamos a los hombres que estan con varias mujeres ", "Gato"),
               ("H", "Postre frio que requiere ser congelado", "Helado"),
               ("I", "Persona triste y amargada", "Infeliz"),
               ("J", "Respirar anhelosamente por efecto del cansancio, la excitación, el calor excesivo ", "Jadear"),
               ("K", "Como estas? Me llego un privado al Instagram...", "Ke personaje"),
               ("L", "SOS UN TANQUE DE ...", "Leche"),
               ("M", "Polvito blanco que se parece a la harina", "Merca"),
               ("N", "Persona de color oscuro", "Negro"),
               ("Ñ", "Apodo de mi amigo el cejas", "Ñandu"),
               ("O", "Cuando miran mucho a personas lindas como nosotras", "Ojear"),
               ("P", "Escasez de pelo ", "Pelado"),
               ("Q", "Equipo de fultbol que descendio en 2017", "Quilmes"),
               ("R", "Vinculo dificil de sostener", "Relacion "),
               ("S", "Marca de vodka que te hace olvidar quien eres", "Smirnoff"),
               ("T", "Boliche pequeño de zona sur", "Target"),
               ("U", "Institucion a la que le tenemos panico", "Universidad"),
               ("V", "Bebida alcoholica que se hace con uvas", "Vino"),
               ("W", "Siempre consigo to lo que quiero", "Wanda Nara"),
               ("X", "Paginas prohibido que miran los hombres", "xxxx"),
               ("Y", "Hierba que se usa para el mate ", "Yerba"),
               ("Z", "Mujeres que tienen muchos hombres", "Zorra"),
             ]


            self.c.executemany("INSERT INTO preguntas                 (letra, pregunta, respuesta) VALUES (?, ?, ?)",             preguntas_ejemplo)
            self.conn.commit()
            self.cargar_preguntas()  # Vuelve a cargar las preguntas después de insertarlas

    def iniciar_juego(self):
        random.shuffle(self.preguntas_respuestas)
        self.siguiente_pregunta()

    def siguiente_pregunta(self):
        if self.preguntas_respuestas:
            self.pregunta_actual = self.preguntas_respuestas.pop(0)
            self.label_pregunta.config(text=f"{self.pregunta_actual[1]}. {self.pregunta_actual[2]}")
        else:
            messagebox.showinfo("Fin del juego", "¡Has completado todas las preguntas!")

    def verificar_respuesta(self):
        if self.pregunta_actual:
            respuesta_usuario = self.respuesta_usuario.get().strip().lower()
            respuesta_correcta = self.pregunta_actual[3].lower()

            if respuesta_usuario == respuesta_correcta:
                messagebox.showinfo("Correcto", "¡Respuesta correcta!")
            else:
                messagebox.showinfo("Incorrecto", f"La respuesta correcta era: {respuesta_correcta}")

            # psa a siguiente pregunta
            self.respuesta_usuario.set("")
            self.siguiente_pregunta()

if __name__ == "__main__":
    root_login = tk.Tk()
    app_login = LoginVentana(root_login)
