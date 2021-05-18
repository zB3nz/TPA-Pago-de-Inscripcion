import conexion
import pdf

conexion = conexion.conectar()
cursor = conexion[1]
database = conexion[0]

class alumno:
    def __init__(self, noControl, nombre = "", apellidos = "", carrera = ""):
        self.noControl = noControl
        self.nombre = nombre
        self.apellidos = apellidos
        self.carrera = carrera
        self.email = ""

    def RegistrarAlumno(self):
        adeudo = self.calcularAdeudo()
        values = (int(self.noControl),self.nombre,self.apellidos,self.carrera,adeudo)
        
        try:
            cursor.execute(f"INSERT INTO alumnos VALUES(%s,%s,%s,%s,%s,null)",values)
            database.commit()
            result = [cursor.rowcount,self]
        except:
            result = [0,self]

        return result

    def RellenarAlumno(self):
        cursor.execute(f"SELECT * FROM alumnos WHERE noControl = '{self.noControl}'")
        datos = cursor.fetchone()

        self.nombre = datos[1]
        self.apellidos = datos[2]
        self.carrera = datos[3]
        self.adeudo = datos[4]
        self.email = datos[5]


    def EliminarAlumno(self):
        cursor.execute(f"DELETE FROM alumnos WHERE noControl = '{self.noControl}'")
        database.commit()
        return cursor.rowcount

    def ActualizarAlumno(self):
        values = (self.nombre, self.apellidos, self.carrera, self.adeudo, self.email, self.noControl)
        cursor.execute("UPDATE alumnos SET nombre = %s, apellidos = %s, carrera = %s, adeudo = %s, email = %s WHERE noControl = %s",values)
        database.commit()
        return cursor.rowcount

    def pagar(self, cantidad, email):
        self.adeudo -= cantidad
        self.email = email
        return self.ActualizarAlumno()

    def calcularAdeudo(self):
        return 2300 + ((int(self.noControl[0:2]) - 10) * 100)

    def acciones(self):

        while True:
            print('\033c')
            print(f"Alumno\n{self.noControl} {self.nombre} {self.apellidos}\t{self.carrera}\tMonto a pagar: ${self.adeudo}")
            print("\n¿Qué desea hacer?\n[1] Pagar inscripción\n[2] Reenviar comprobante de pago\n\n[3] Regresar\n")
            opcion = input()
            print('\033c')

            #Pagar inscripcion
            if opcion == "1":
                if self.adeudo <= 0:
                    print("Este alumno ya tiene pagada su inscripción.")
                else:
                    self.pagoConsola()
            
            #Reenviar ticket
            elif opcion == "2":
                if self.email == None or self.email.replace(" ","") == "":
                    print("No se ha registrado ningún pago.")
                else:
                    print(f"Se reenviará un comprobante de pago al último correo registrado al pagar ({self.email})")
                    #Enviar al correo
                    self.generarComprobante()

            #Regresar
            elif opcion == "3":
                return
            
            else:
                print("No escogió ninguna opción.")

            input("\nPresione enter para continuar.")

    def pagoConsola(self):
        input("Ingrese los datos de su tarjeta:\nNúmero de tarjeta (16 digitos): ")
        input("Nombre y apellido del titular: ")
        input("Fecha de expiración (MM/AA): ")
        input("Código de seguridad (3 digitos): ")

        print('\033c')

        cantidad = int(input("\nIngrese la cantidad que desea pagar: $"))
        email = input("Ingrese un correo para envíar su comprobante de pago: ")

        print("\nConfirmando pago...")
        
        if self.pagar(cantidad, email) == 0:
            print("Ocurrió un error al actualizar los datos.")
            return

        input("Pago completado. Presione enter para continuar.")
        self.generarComprobante()

    def generarComprobante(self):
        print("\nGenerando comprobante de pago")
        
        try:
            fname = pdf.generarTicket(self)
            print(f"Comprobante generado en {fname}")
        except:
            print("Fallo al generar el comprobante.")