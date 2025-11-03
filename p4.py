import datetime, threading, requests, json, subprocess, time, os

#globales
ficheros = []
url="http://localhost:5000/"
intervalo_api=0.1
intervalo_ficheros=2
carpeta="ficheros/"
tablas="res.partner sale.order sale.order.line account.move res.users product.product"

def getApi(tabla):
    global url
    d={
        "user":"ikmssaid24@lhusurbil.eus",
        "password":"usuario"
    }
    a= requests.post(url+"login", json=d)
    v=a.cookies
    a= requests.get(url+"getDatosFiltro/"+tabla,cookies=v )
    return json.dumps(a.json(), indent=4)

def generarfichero(nom_tabla):
    nom_fich=nom_tabla+datetime.datetime.now().strftime("%Y%m%d")+".json"
    d=getApi(nom_tabla)
    with open(carpeta+nom_fich, "w+", encoding="utf-8") as f:
        f.write(d)

def generarficheros():
    while True:
        for tabla in tablas.split(" "):
            generarfichero(tabla)
        time.sleep(intervalo_api*60)


def monitorizar_ficheros():
    os.makedirs(carpeta, exist_ok=True)
    while True:
        for fichero in os.listdir(carpeta):
            if fichero.endswith(".json") and fichero not in ficheros:
                ficheros.append(fichero)
                print(f"fichero detectado: {fichero}")
        time.sleep(intervalo_ficheros)  # revisa cada 2 segundos

def mostrar_ficheros(numeros=False):
    print(f""".
└── {carpeta}""")
    for i in range(len(ficheros)):
        if numeros:
            if i<len(ficheros)-1:
                print(f"\t├──[{i}]", ficheros[i])
            else:
                print( f"\t└──[{i}]", ficheros[i], "\n")
        else:
            if i<len(ficheros)-1:
                print("\t├──", ficheros[i])
            else:
                print( "\t└──", ficheros[i], "\n")

def aniadir():
    mostrar_ficheros()
    nombre=input("\nIntroduzca el nombre del nuevo fichero:")
    try:
        with open(carpeta+nombre, "x"):
            ficheros.append(nombre)
            print(f"El fichero {nombre} ha sido creado correctamente")
    except:
        print("Error, fallo en la operacion, asegurese de que no haya un fichero con el mismo nombre...")

def editar():
    mostrar_ficheros(True)
    try:
        i=int(input("\nIntroduzca el numero del fichero a editar:"))
        if i<0:
            print("Error, valor mal introducido...")
            return
        fich=carpeta+ficheros[i]
        if not os.path.exists(fich):
            print("El fichero no existe.")
            return
        subprocess.run(["notepad.exe", fich])
    except:
        print("Error, no se ha podido realizar la operacion...")

def eliminar():
    try:
        mostrar_ficheros(True)
        i=int(input("\nIntroduzca el fichero a eliminar:"))
        if i<0:
            print("Error, valor mal introducido...")
            return
        fich=carpeta+ficheros[i]
        if os.path.exists(fich):
            os.remove(fich)
            print(f"Fichero \"{ficheros.pop(i)}\" eliminado correctamente...")
        else:
            print("Error, el fichero no existe...")
    except:
        print("Error la operacion no se ha podido completar...")

def menu_ficheros():
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


def configuracion():
    global url, intervalo_api, intervalo_ficheros, carpeta, tablas
    while True:
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
                    try:
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
                    try:
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


def ping():
    try:
        url_ping=input("Introduzca la url a la que quiere hacer el ping:")
        salida = subprocess.run(["ping", "-n", "2", url_ping ], capture_output=True, text=True)
        print( salida.stdout)
    except:
        print("Error no se ha podido realizar la operacion...")

def mostrar_menu():
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


if __name__=="__main__":
    threading.Thread(target=generarficheros, daemon=True).start()
    threading.Thread(target=monitorizar_ficheros, daemon=True).start()
    time.sleep(2)
    mostrar_menu()
        