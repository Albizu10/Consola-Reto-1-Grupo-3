import datetime, threading, requests, json, subprocess, time, os

# -*- coding: utf-8 -*-

#globales
ficheros = []
url="https://api-grupo3.duckdns.org/"
intervalo_api=0.1
intervalo_ficheros=2
carpeta="ficheros/"
tablas="res.partner sale.order sale.order.line account.move res.users product.product"
#funcion para conectarse a la api y obtener los datos
def getApi(tabla):
    global url
    d={
        "user":"ikmssaid24@lhusurbil.eus",
        "password":"usuario"
    }
    a= requests.post(url+"login", json=d)#realizo login pasandole usuario y contrasenia
    v=a.cookies#guardo la coockie
    a= requests.get(url+"getDatosFiltro/"+tabla,cookies=v)# hago el get pasandole la cookie
    return json.dumps(a.json(), indent=4)

def generarfichero(nom_tabla):#funcion que crea o modifica un fichero y introduce en el los datos obtenidos de la api
    nom_fich=nom_tabla+datetime.datetime.now().strftime("%Y%m%d")+".json"# hago el noombre del fichero (tabla+fecha).json
    d=getApi(nom_tabla)#asigno los datos obtenidos por la api
    with open(carpeta+nom_fich, "w+", encoding="utf-8") as f:#w para crear el fichero si no existe  
        f.write(d)

def generarficheros():#funcion que genera la cantidad de ficheros segun la variable tabla
    while True:
        for tabla in tablas.split(" "):
            generarfichero(tabla)
        time.sleep(intervalo_api*60)#intervalo de descarga de datos de la api


def monitorizar_ficheros():#funcion para que acada x tiempo revise si existen ficharos nuevos que se han aniadido y los guarfa en la variable ficheros
    os.makedirs(carpeta, exist_ok=True)
    while True:
        for fichero in os.listdir(carpeta):
            if fichero.endswith(".json") and fichero not in ficheros:
                ficheros.append(fichero)
                print(f"fichero detectado: {fichero}")
        time.sleep(intervalo_ficheros)  # para x segundos y vuelve a ejecutar

def mostrar_ficheros(numeros=False):#funcion que se encarga de mostrar por pantalla todos los ficheros
    print(f""".
└── {carpeta}""")
    for i in range(len(ficheros)):
        if numeros:# lo separo por la variable numeros para mostrar el numero correspondiente al fichero o no
            if i<len(ficheros)-1:
                print(f"\t├──[{i}]", ficheros[i])
            else:
                print( f"\t└──[{i}]", ficheros[i], "\n")
        else:
            if i<len(ficheros)-1:
                print("\t├──", ficheros[i])
            else:
                print( "\t└──", ficheros[i], "\n")

def aniadir():#funcion para aniadir nuevos ficheros al directorio
    mostrar_ficheros()
    nombre=input("\nIntroduzca el nombre del nuevo fichero:")
    try:
        with open(carpeta+nombre, "x"):#aqui con x para que lance error si ya existe el fichero
            ficheros.append(nombre)
            print(f"El fichero {nombre} ha sido creado correctamente")
    except:
        print("Error, fallo en la operacion, asegurese de que no haya un fichero con el mismo nombre...")

def editar():#funcion para editar el contenido de un fichero
    mostrar_ficheros(True)
    try:
        i=int(input("\nIntroduzca el numero del fichero a editar:"))#recojo la posicion relacionada con el fichero a editar
        if i<0:
            print("Error, valor mal introducido...")
            return
        fich=carpeta+ficheros[i]#asigno la ruta desde el directorio actual y me aseguro de que existe
        if not os.path.exists(fich):
            print("El fichero no existe.")
            return
        subprocess.run(["notepad.exe", fich])#lo ejecuto con el bloc de notas
    except:
        print("Error, no se ha podido realizar la operacion...")

def eliminar():#funcion para eliminar un fichero
    try:
        mostrar_ficheros(True)
        i=int(input("\nIntroduzca el fichero a eliminar:"))
        if i<0:
            print("Error, valor mal introducido...")#control de errores
            return
        fich=carpeta+ficheros[i]
        if os.path.exists(fich):
            os.remove(fich)
            print(f"Fichero \"{ficheros.pop(i)}\" eliminado correctamente...")#el pop para eliminarlo y poder mostrar despues la correcta eliminacion de fichero
        else:
            print("Error, el fichero no existe...")
    except:
        print("Error la operacion no se ha podido completar...")

def menu_ficheros():#funcion para navegacion entre las opciones de la opcion 1-ficheros
    while True:
        try:
            opc=int(input("""\nIntroduzca una opcion:
    0-Atras
    1-Aniadir
    2-Editar 
    3-Eliminar
    :"""))  
            if opc==0:
                break
            elif opc==1:
                aniadir()
            elif opc==2:
                editar()
            elif opc==3:
                eliminar()
            else:
                print("Opcion incorrecta vuelva a interntarlo...")
                continue
        except:
            print("Opcion incorrecta vuelva a interntarlo...")
            continue


def configuracion():#funcion que cambia la configuracion cambiando las variables globales
    global url, intervalo_api, intervalo_ficheros, carpeta, tablas
    while True:#bucle para elegir cambiar algo o volver atras
        print(f"""
              ATENCION NO NOS HACEMOS CARGO DEL MAL USO QUE SE LE PUEDA DAR A LA APLICACION 
              Si usted cambia algun parametro y la aplicacion deja de funcionar reiniciela y
              revise bien los parametros que quiere introducir

    0-Url de la API: \"{url}\"
    1-Intervalo bajada de datos: {intervalo_api} minutos
    2-Intervalo de comprobacion de ficheros: {intervalo_ficheros} minutos
    3-Carpeta por defecto: \"{carpeta}\" 
    4-Tablas de la API a almacenar: \"{tablas}\"
    5-Volver atras
    """)
        try:
            opc=int(input("Seleccione una opcion:"))
            if opc==0:
                    try:#basicamente asigna el input a la global y ya
                        i=input("""
                              ¡Atencion! esta a punto de cambiar parametros importantes para el buen funcionamiento de la aplicacion
                              asegurese de que sus datos sean correctos antes de cambiarlos.
                              \n
                                Itroduzca la url de la api a la que se quiere conectar(e.j. http://ejwmplo.com)
                                :""")
                        url=i
                    except:
                        print("Los datos han sido mal introducidos, aviso, los cambios no se van a efectuar")
            elif opc==1:
                    try:#y aqui necesito pasarlo a int
                        i=int(input("""
                              ¡Atencion! esta a punto de cambiar parametros importantes para el buen funcionamiento de la aplicacion
                              asegurese de que sus datos sean correctos antes de cambiarlos.
                              \n
                                Introduzca en minutos el intervalo de tiempo de descarga de los archivos
                                :"""))
                        intervalo_api=i
                    except:
                        print("Los datos han sido mal introducidos, aviso, los cambios no se van a efectuar")
            elif opc==2:
                    try:
                        i=int(input("""
                              ¡Atencion! esta a punto de cambiar parametros importantes para el buen funcionamiento de la aplicacion
                              asegurese de que sus datos sean correctos antes de cambiarlos.
                              \n
                                Inroduzca en segundos el intervalo de verificacion de ficheros nuevos"""))
                        intervalo_ficheros=i
                    except:
                        print("Los datos han sido mal introducidos, aviso, los cambios no se van a efectuar")
            elif opc==3:
                    try:
                        i=input("""
                              ¡Atencion! esta a punto de cambiar parametros importantes para el buen funcionamiento de la aplicacion
                              asegurese de que sus datos sean correctos antes de cambiarlos.
                              \n
                               Introduzca el directorio en el que quiere guerdar los archivos :""")
                        carpeta=i
                    except:
                        print("Los datos han sido mal introducidos, aviso, los cambios no se van a efectuar")
            elif opc==4:
                    try:
                        i=input("""
                              ¡Atencion! esta a punto de cambiar parametros importantes para el buen funcionamiento de la aplicacion
                              asegurese de que sus datos sean correctos antes de cambiarlos.
                              \n
                               Introduzca las tablas a guardar separadas por un espacio entre ellas :""")
                        tablas=i
                    except:
                        print("Los datos han sido mal introducidos, aviso, los cambios no se van a efectuar")
            elif opc==5:
                    break
            else:
                    print("Opcion incorrecta vuelva a interntarlo...")
                    continue
        except:
                print("Opcion incorrecta vuelva a interntarlo...")
                continue


def ping():#funcion que realiza un ping a un dominio y no url
    try:
        ping=input("Introduzca el dominio al que quiere hacer el ping(Sin 'http(s)://'):")
        salida = subprocess.run(["ping", "-n", "2", ping ], capture_output=True, text=True)#ejecuto el ping con parametros -n y 2 para solo dos requests
        print( salida.stdout)
    except:
        print("Error no se ha podido realizar la operacion...")

def mostrar_menu():#funcion que muestra el menu y controla la opciones ejecutando una funcion segun la opcion introducida
    while True:
        try:
            opc=int(input("""
    0-Salir
    1-Ficheros
    2-Configuracion
    3-Ping
    """))
            if opc==0:
                break
            elif opc==1:
                menu_ficheros()
            elif opc==2:
                configuracion()
            elif opc==3:
                ping()
            else:
                print("Opcion incorrecta vuelva a interntarlo...")
                continue
        except:
            print("Opcion incorrecta vuelva a interntarlo...")
            continue


if __name__=="__main__":#aqui empieza la aplcacion
    threading.Thread(target=generarficheros, daemon=True).start()#ejecuto las funciones generar... y monitorizar... en un thread para que se ejecute en segundo plano y la aplicacion siga funcionando
    threading.Thread(target=monitorizar_ficheros, daemon=True).start()
    time.sleep(2)#le pongo un sleep para que le de tiempo a monitorizar a detectar los ficheros y no rompa el menu con los prints
    mostrar_menu()#inicio la funcion principal
        