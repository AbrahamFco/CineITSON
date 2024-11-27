import tkinter as tk
from tkinter import messagebox, simpledialog

class CineVIP:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Cine ITSON")
        self.raiz.geometry("800x600")

        self.asiento = tk.PhotoImage(file="silla.png") 
        self.asiento_ocupado = tk.PhotoImage(file="sillaOcupada.png")  
        self.seleccionar = tk.PhotoImage(file="seleccion.png")
        self.historial = tk.PhotoImage(file="historial.png") 
        self.recuento = tk.PhotoImage(file="recuento.png")
        self.funcion_imagenes = [
                tk.PhotoImage(file="venom.png"),
                tk.PhotoImage(file="sonrie.png"),
                tk.PhotoImage(file="gladiador.png")
            ]

        self.funciones = [
            {"nombre": "Venom el último baile", "horario": "2:00 PM", "asientos": [True] * 16, "boletos_vendidos": []},
            {"nombre": "Sonríe 2", "horario": "5:00 PM", "asientos": [True] * 16, "boletos_vendidos": []},
            {"nombre": "Gladiador (ReEstreno)", "horario": "8:00 PM", "asientos": [True] * 16, "boletos_vendidos": []}
        ]
        self.boton_seleccion_funcion = tk.Button(self.raiz, text="Seleccionar Funcion", image=self.seleccionar, compound="top", command=self.mostrar_funciones)
        self.boton_seleccion_funcion.pack(pady=(80, 10))
        self.boton_historial = tk.Button(self.raiz, text="Historial de Ventas", image=self.historial, compound="top", command=self.mostrar_historial)
        self.boton_historial.pack(pady=(80, 10))
        self.boton_recuento = tk.Button(self.raiz, text="Recuento de Ventas", image=self.recuento, compound="top", command=self.mostrar_recuento)
        self.boton_recuento.pack(pady=(80, 0))

    def mostrar_funciones(self):
        ventana_funciones = tk.Toplevel(self.raiz)
        ventana_funciones.title("Funciones Disponibles")
        ventana_funciones.geometry("500x700")
        for seleccionado, funcion in enumerate(self.funciones):
            nombre_funcion = f"{funcion['nombre']} - {funcion['horario']}"
            boton_funcion = tk.Button(ventana_funciones, text=nombre_funcion, image=self.funcion_imagenes[seleccionado], command=lambda seleccionado=seleccionado: self.seleccionar_asiento(seleccionado))
            boton_funcion.pack(pady=5)

    def seleccionar_asiento(self, seleccionado):
        ventana_asientos = tk.Toplevel(self.raiz)
        ventana_asientos.title("Seleccionar Asiento")
        ventana_asientos.geometry("500x500")
        funcion = self.funciones[seleccionado]
        tk.Label(ventana_asientos, text=f"Selecciona un asiento para {funcion['nombre']} - {funcion['horario']}").pack(pady=10)
        frame_asientos = tk.Frame(ventana_asientos)
        frame_asientos.pack(pady=10)

        self.botones_asientos = []
        for i in range(4):
            fila_botones = []
            for j in range(4):
                asiento_seleccionado = i * 4 + j
                imagen = self.asiento if funcion['asientos'][asiento_seleccionado] else self.asiento_ocupado
                boton_asiento = tk.Button(
                    frame_asientos, 
                    image=imagen, 
                    text=f"{asiento_seleccionado + 1}",
                    compound="top",
                    width=80, 
                    height=80, 
                    state=(tk.NORMAL if funcion['asientos'][asiento_seleccionado] else tk.DISABLED), 
                    command=lambda asiento_seleccionado=asiento_seleccionado, seleccionado=seleccionado: self.vender_boleto(seleccionado, asiento_seleccionado, frame_asientos)
                )
                boton_asiento.grid(row=i, column=j, padx=5, pady=5)
                fila_botones.append(boton_asiento)
            self.botones_asientos.append(fila_botones)

    def vender_boleto(self, seleccionado, asiento_numero, frame_asientos):
        nombre_cliente = simpledialog.askstring("Nombre del Cliente", "Ingrese el nombre del cliente (opcional):")
        if not nombre_cliente:
            nombre_cliente = "SinNumeroCliente"

        funcion = self.funciones[seleccionado]
        funcion['asientos'][asiento_numero] = False
        boleto = {
            "cliente": nombre_cliente, 
            "asiento": asiento_numero + 1, 
            "precio": 80.0
        }
        funcion['boletos_vendidos'].append(boleto)
        # falta arreglar error en el boton de ocupado
        fila = asiento_numero // 4
        columna = asiento_numero % 4
        self.botones_asientos[fila][columna].config(state=tk.DISABLED, image=self.asiento_ocupado, text=f"{asiento_numero + 1} (Ocupado)")

        messagebox.showinfo("Boleto Vendido", f"Boleto vendido para {funcion['nombre']} - Asiento {asiento_numero + 1}\nCliente: {nombre_cliente}\nPrecio: $80.0")

    def mostrar_historial(self):
        ventana_historial = tk.Toplevel(self.raiz)
        ventana_historial.title("Historial de Ventas")
        ventana_historial.geometry("600x400")
        for funcion in self.funciones:
            for boleto in funcion['boletos_vendidos']:
                texto_boleto = f"Cliente: {boleto['cliente']}, Funcion: {funcion['nombre']}, Asiento: {boleto['asiento']}, Precio: ${boleto['precio']}"
                tk.Label(ventana_historial, text=texto_boleto).pack(pady=2)

    def mostrar_recuento(self):
        ventana_recuento = tk.Toplevel(self.raiz)
        ventana_recuento.title("Recuento de Ventas")
        ventana_recuento.geometry("600x400")
        for funcion in self.funciones:
            cantidad_vendida = len(funcion['boletos_vendidos'])
            ganancia_total = sum(boleto['precio'] for boleto in funcion['boletos_vendidos'])
            texto_funcion = f"Funcion: {funcion['nombre']} - {funcion['horario']}, Boletos vendidos: {cantidad_vendida}, Ganancia: ${ganancia_total}"
            tk.Label(ventana_recuento, text=texto_funcion).pack(pady=5)

if __name__ == "__main__":
    raiz = tk.Tk()
    app = CineVIP(raiz)
    raiz.mainloop()