import conexion
import hashlib
import alumno

conexion = conexion.conectar()
cursor = conexion[1]
database = conexion[0]

class administrador:
    def __init__(self, usuario, password):
        self.usuario = usuario
        self.password = password

        self.ExistenAdministradores()

    def ConfirmarSesion(self):
        cifrado = hashlib.sha256()
        cifrado.update(self.password.encode('utf8'))
        
        values = (self.usuario,cifrado.hexdigest())
        cursor.execute("SELECT * FROM administradores WHERE usuario = %s AND password = %s",values)
        
        return cursor.fetchone()

    def CrearAdministrador(self):
        cifrado = hashlib.sha256()
        cifrado.update(self.password.encode('utf8'))
        
        try:
            values = (self.usuario, cifrado.hexdigest())
            cursor.execute(f"INSERT INTO administradores VALUES(null, %s, %s)",values)
            database.commit()
            result = [cursor.rowcount,self]
        except:
            result = [0,self]

        return result

    def EliminarCuenta(self):
        cursor.execute(f"DELETE FROM administradores WHERE usuario = '{self.usuario}'")
        database.commit()

    def ExistenAdministradores(self):
        cursor.execute("SELECT * FROM administradores")
        
        if len(cursor.fetchall()) == 0:
            input("Se ha creado una cuenta con las credenciales que ha ingresado debido a que no existen actualmente administradores.")
            self.CrearAdministrador()

    def acciones(self):
        while True:
            print('\033c')
            print("¿Qué desea hacer?\n[1] Buscar alumnos\n[2] Registrar alumno\n[3] Editar alumno")
            print("[4] Eliminar alumno\n\n[5] Cerrar sesión\n[6] Registrar administrador \n[7] Borrar cuenta\n")
            opcion = input()
            print('\033c')

            #Buscar alumnos
            if opcion == "1":
                self.BuscarAlumnos()
                continue

            #Registrar alumnos
            elif opcion == "2":
                try:
                    noControl = int(input("Rellene el siguiente formulario para registrar al alumno.\nNumero de control: "))
                    assert noControl > 9

                    nombre = input("Nombre: ")
                    apellidos = input("Apellidos: ")
                    carrera = input("Carrera: ")

                except:
                    input("Datos incorrectos, verifiquelos.")
                    continue

                miAlumno = alumno.alumno(str(noControl),nombre,apellidos,carrera)
                registro = miAlumno.RegistrarAlumno()

                if registro[0] >= 1:
                    print(f"\nEl alumno {registro[1].noControl} ha sido registrado satisfactoriamente con un adeudo de ${registro[1].calcularAdeudo()}.")
                else:
                    print("\nNo se ha podido completar el registro.")

            #Editar alumno
            elif opcion == "3":
                noControl = input("Ingrese el numero de control del alumno que quiere editar: ")
                miAlumno = alumno.alumno(noControl)
                
                try:
                    miAlumno.RellenarAlumno()

                    try:
                        miAlumno.nombre = input(f"Nombre ({miAlumno.nombre}): ")
                        miAlumno.apellidos = input(f"Apellidos ({miAlumno.apellidos}): ")
                        miAlumno.carrera = input(f"Carrera ({miAlumno.carrera}): ")
                        miAlumno.adeudo = int(input(f"Adeudo ({miAlumno.adeudo}): "))
                        miAlumno.email = input(f"Correo ({miAlumno.email}): ")

                    except:
                        input("Datos incorrectos, verifiquelos.")
                        continue

                    if miAlumno.ActualizarAlumno() == 0:
                        print("\nOcurrió un error al actualizar los datos.")
                    else:
                        print("\nDatos actualizados correctamente.")

                except:
                    print(f"No se encontró ningún alumno con el número de control {noControl}")


            #Eliminar alumnos
            elif opcion == "4":
                noControl =  input("Ingrese el numero de control del alumno que quiere eliminar: ")
                miAlumno = alumno.alumno(noControl)
                resultado = miAlumno.EliminarAlumno()

                print("\nNo se ha encontrado ningun alumno con ese número de control." if resultado == 0 else "\nSe ha eliminado correctamente.")

            #Cerrar sesión
            elif opcion == "5":
                return

            #Registrar administrador
            elif opcion == "6":
                usuario = input("Ingrese el usuario del nuevo administrador: ")
                password = input("Ingrese una contraseña para la nueva cuenta: ")
                
                admin = administrador(usuario, password)
                registro = admin.CrearAdministrador()

                if registro[0] >= 1:
                    print(f"\nEl administrador {registro[1].usuario} ha sido registrado satisfactoriamente.")
                else:
                    print("\nNo se ha podido completar el registro.")

            #Eliminar cuenta
            elif opcion == "7":
                password = input("Ingrese su contraseña para confirmar la eliminación de su cuenta: ")
                if password == self.password:
                    self.EliminarCuenta()
                    input("\nCuenta eliminada satisfactoriamente.")
                    return
                else:
                    print("\nHa ingresado una contraseña incorrecta.")
            
            else:
                print("\nHas seleccionado una opción incorrecta.")

            input("\nPresione enter para continuar.")

    def BuscarAlumnos(self):
        while True:
            sql = "SELECT * FROM alumnos "

            print('\033c')
            print("[1] Mostrar todos los alumnos\n\n[2] Buscar por número de control\n[3] Buscar por nombre\n[4] Buscar por apellidos")
            print("[5] Buscar por carrera\n\n[6] Mostrar deudores\n[7] Mostrar ya pagados\n\n[8] Regresar\n")
            opcion = input()
            print('\033c')

            #Mostrar todos
            if opcion == "1":
                pass

            #Buscar por no. Control
            elif opcion == "2":
                noControl = input("Ingrese el numero de control por donde comenzar a buscar (ej. 17, 18100): ")
                sql += f"WHERE CONVERT(noControl, char(10)) LIKE '{noControl}%'"

            #Buscar por nombre
            elif opcion == "3":
                nombre = input("Ingrese el nombre del alumno: ")
                sql += f"WHERE nombre LIKE '%{nombre}%'"
            
            #Buscar por apellido
            elif opcion == "4": 
                apellido = input("Ingrese el apellido del alumno: ")
                sql += f"WHERE apellidos LIKE '%{apellido}%'"
            
            #Buscar por carrera
            elif opcion == "5": 
                carrera = input("Ingrese la carrera del alumno: ")
                sql += f"WHERE carrera LIKE '%{carrera}%'"
            
            #Mostrar deudores
            elif opcion == "6":
                print("Deudores")
                sql += f"WHERE adeudo > 0"
            
            #Mostrar los que pagaron
            elif opcion == "7":
                print("Pagados")
                sql += f"WHERE adeudo <= 0"
            
            #Regresar
            elif opcion == "8":
                return

            else:
                input("No escogiste ninguna opción. Presione enter para continuar.")
                continue
            
            cursor.execute(sql)
            self.ImprimirAlumnos(cursor.fetchall())

            input("\nPresione enter para continuar.")

    def ImprimirAlumnos(self, rows):

        if len(rows) == 0:
            print("\nNo se encontraron resultados para la búsqueda.")
            return

        print("\nNo. Control\tNombre\t\tApellidos\tCarrera\tAdeudo\te-mail")
        for a in rows:
            print(f"{a[0]}\t{a[1][:7]}\t\t{a[2][:7]}\t\t{a[3]}\t${a[4]}\t{a[5]}")
