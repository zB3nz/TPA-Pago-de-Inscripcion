import administrador
import alumno

while True:
    print('\033c')
    print("""\nBienvenido al sistema de pago de inscripciones\n\n¿Qué desea hacer?:
[1] Pagar inscripción de alumno
[2] Ingresar como administrador\n""")

    opcion = input()
    print('\033c')

    if opcion == "1":
        try:
            noControl = int(input("Ingrese el numero de control: "))
            assert noControl > 9

            miAlumno = alumno.alumno(str(noControl))
            miAlumno.RellenarAlumno()

            miAlumno.acciones()
            continue
        except:
            print("No se encontró ningun alumno con ese numero de control.")

    elif opcion == "2":
        usuario = input("Ingrese su usuario: ")
        password = input("Ingrese su contraseña: ")

        admin = administrador.administrador(usuario, password)
        login = admin.ConfirmarSesion()

        if login == None:
            print("Credenciales incorrectas")
        else:
            input(f"\nBienvenido {login[1]}, presione enter para continuar.")
            admin.acciones()
            continue

    else:
        print("No escogió ninguna opción.")

    input("\nPresione enter para continuar.")
        