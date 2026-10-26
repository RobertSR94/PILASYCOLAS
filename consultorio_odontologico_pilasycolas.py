    from datetime import date, timedelta

class Cliente:
    def __init__(self, id_cliente, nombre, telefono, procedimiento,
                 prioridad, fecha, hora):
        self.id = id_cliente
        self.nombre = nombre
        self.telefono = telefono
        self.procedimiento = procedimiento      # "Extracción", "Limpieza", ...
        self.prioridad = prioridad              # "Urgente" o "Normal"
        self.fecha = fecha                      # datetime.date
        self.hora = hora                        # "HH:MM"

    def __str__(self):
        return (f"[{self.id}] {self.nombre:<18} Tel: {self.telefono:<11} "
                f"{self.procedimiento:<11} {self.prioridad:<8} "
                f"{self.fecha.isoformat()} {self.hora}")


class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class Pila:
    def __init__(self):
        self.tope = None
        self.tamano = 0

    def esta_vacia(self):
        return self.tope is None

    def push(self, dato):                 # apilar
        nodo = Nodo(dato)
        nodo.siguiente = self.tope
        self.tope = nodo
        self.tamano += 1

    def pop(self):                        # desapilar
        if self.esta_vacia():
            return None
        nodo = self.tope
        self.tope = nodo.siguiente
        self.tamano -= 1
        return nodo.dato

    def peek(self):                       # ver el tope sin sacarlo
        return None if self.esta_vacia() else self.tope.dato

    def recorrer(self):                   # del tope hacia el fondo
        actual = self.tope
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente


class Cola:
    def __init__(self):
        self.frente = None
        self.final = None
        self.tamano = 0

    def esta_vacia(self):
        return self.frente is None

    def encolar(self, dato):
        nodo = Nodo(dato)
        if self.esta_vacia():
            self.frente = nodo
        else:
            self.final.siguiente = nodo
        self.final = nodo
        self.tamano += 1

    def desencolar(self):
        if self.esta_vacia():
            return None
        nodo = self.frente
        self.frente = nodo.siguiente
        if self.frente is None:
            self.final = None
        self.tamano -= 1
        return nodo.dato

    def ver_frente(self):
        return None if self.esta_vacia() else self.frente.dato

    def recorrer(self):                   # del frente hacia el final
        actual = self.frente
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

def cargar_clientes():
    hoy = date.today()
    d = lambda n: hoy + timedelta(days=n)
    return [
        Cliente(1, "Ana Gómez",       "3001112233", "Extracción", "Urgente", d(5),  "09:00"),
        Cliente(2, "Carlos Ruiz",     "3012223344", "Limpieza",   "Normal",  d(0),  "08:00"),
        Cliente(3, "Marta Londoño",   "3023334455", "Extracción", "Urgente", d(1),  "10:30"),
        Cliente(4, "Julián Pérez",    "3034445566", "Extracción", "Normal",  d(2),  "11:00"),
        Cliente(5, "Sofía Restrepo",  "3045556677", "Extracción", "Urgente", d(12), "14:00"),
        Cliente(6, "Luis Herrera",    "3056667788", "Ortodoncia", "Urgente", d(0),  "09:30"),
        Cliente(7, "Paula Mejía",     "3067778899", "Extracción", "Urgente", d(3),  "15:30"),
        Cliente(8, "Andrés Vélez",    "3078889900", "Calzas",     "Normal",  d(0),  "10:00"),
        Cliente(9, "Daniela Ossa",    "3089990011", "Extracción", "Urgente", d(0),  "11:30"),
        Cliente(10, "Mateo Cardona",  "3090001122", "Extracción", "Normal",  d(0),  "08:30"),
    ]

def construir_pila(clientes):
    
    urgentes = [c for c in clientes
                if c.procedimiento == "Extracción" and c.prioridad == "Urgente"]
    urgentes.sort(key=lambda c: (c.fecha, c.hora), reverse=True)
    pila = Pila()
    for c in urgentes:
        pila.push(c)
    return pila


def generar_informe_pila(pila, archivo="informe_pila.txt"):
    lineas = []
    lineas.append("=" * 78)
    lineas.append("INFORME DE PILA - EXTRACCIONES URGENTES")
    lineas.append(f"Generado: {date.today().isoformat()}   "
                  f"Clientes en pila: {pila.tamano}")
    lineas.append("Orden de llamada: del TOPE (fecha más cercana) al FONDO")
    lineas.append("=" * 78)
    if pila.esta_vacia():
        lineas.append("No hay clientes urgentes de extracción pendientes.")
    for pos, c in enumerate(pila.recorrer(), start=1):
        marca = "  <-- TOPE" if pos == 1 else ""
        lineas.append(f"{pos:>2}. {c}{marca}")
    lineas.append("=" * 78)
    texto = "\n".join(lineas)
    with open(archivo, "w", encoding="utf-8") as f:
        f.write(texto + "\n")
    return texto

def construir_cola_agenda(clientes, fecha):
    """Agenda del día: clientes con cita en 'fecha', encolados por hora."""
    del_dia = [c for c in clientes if c.fecha == fecha]
    del_dia.sort(key=lambda c: c.hora)
    cola = Cola()
    for c in del_dia:
        cola.encolar(c)
    return cola

def mostrar_estructura(titulo, iterable):
    print(f"\n--- {titulo} ---")
    vacio = True
    for i, c in enumerate(iterable, start=1):
        print(f"{i:>2}. {c}")
        vacio = False
    if vacio:
        print("(vacía)")


def registrar_cliente(clientes):
    try:
        nuevo_id = max((c.id for c in clientes), default=0) + 1
        nombre = input("Nombre: ").strip()
        tel = input("Teléfono: ").strip()
        proc = input("Procedimiento (Extracción/Limpieza/Calzas/...): ").strip()
        prio = input("Prioridad (Urgente/Normal): ").strip().capitalize()
        fecha = date.fromisoformat(input("Fecha (AAAA-MM-DD): ").strip())
        hora = input("Hora (HH:MM): ").strip()
        clientes.append(Cliente(nuevo_id, nombre, tel, proc, prio, fecha, hora))
        print("Cliente registrado.")
    except ValueError:
        print("Fecha inválida. Use el formato AAAA-MM-DD.")


def menu():
    print("""
=========== CONSULTORIO ODONTOLÓGICO ===========
1. Ver todos los clientes
2. Registrar cliente
3. Generar PILA de urgencias y informe (informe_pila.txt)
4. Llamar al siguiente de la PILA (pop)
5. Generar COLA de la agenda del día
6. Atender al siguiente de la COLA (desencolar)
7. Ver COLA actual
0. Salir""")
    return input("Opción: ").strip()


def main():
    clientes = cargar_clientes()
    pila = Pila()
    cola = Cola()

    while True:
        op = menu()
        if op == "1":
            mostrar_estructura("CLIENTES REGISTRADOS", clientes)
        elif op == "2":
            registrar_cliente(clientes)
        elif op == "3":
            pila = construir_pila(clientes)
            print(generar_informe_pila(pila))
            print("Informe guardado en informe_pila.txt")
        elif op == "4":
            c = pila.pop()
            if c is None:
                print("La pila está vacía (genere la pila con la opción 3).")
            else:
                print(f"\nLLAMAR A: {c}")
                print(f"Quedan {pila.tamano} cliente(s) en la pila.")
        elif op == "5":
            entrada = input("Fecha de la agenda (AAAA-MM-DD, Enter = hoy): ").strip()
            try:
                f = date.fromisoformat(entrada) if entrada else date.today()
            except ValueError:
                print("Fecha inválida.")
                continue
            cola = construir_cola_agenda(clientes, f)
            mostrar_estructura(f"AGENDA {f.isoformat()} (FRENTE -> FINAL)",
                               cola.recorrer())
        elif op == "6":
            c = cola.desencolar()
            if c is None:
                print("No hay clientes en la cola (genere la agenda con la opción 5).")
            else:
                print(f"\nATENDIENDO: {c}")
                print(f"Quedan {cola.tamano} cliente(s) en la cola.")
        elif op == "7":
            mostrar_estructura("COLA DE ATENCIÓN (FRENTE -> FINAL)", cola.recorrer())
        elif op == "0":
            print("Hasta luego.")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
