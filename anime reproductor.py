#------------------------------------------------------------------
#MODULOS
#------------------------------------------------------------------
import os
import re #para usar expresiones regulares
from colorama import Fore #para aplicar colores
import requests #hacer peticiones http
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from webbrowser import open
#------------------------------------------------------------------
#FUNCIONES
#------------------------------------------------------------------

#esta funcion se encarga de ver si el digito pertenece a un titulo o no MONOS CHINOS
def existe_titulo(digito, titulos):
    if titulos == []:
        return False
    for i in titulos:
        if digito == str(i[0]):
            return i[1]
    return False

#esta funcion se encarga de abrir el link de la serie escogida MONOS CHINOS
def abrir_link(serie, website):
    web_p1 = "https://monoschinos2.com/anime/"
    web_p2 = "-sub-espanol" 

    abc = "abcdefghijklmnñopqrstuvwxyz- "
    abc_mayus = abc.upper()
    nums = "1234567890"
    #reescribimos la serie sin caracteres especiales para poder buscar su link
    serie_final = ""
    for i in serie:
        if i in abc or i in abc_mayus or i in nums:
            serie_final += i
    serie_final = serie_final.lower()
    serie_final = serie_final.replace(" ", "-")

    #completamos el link
    web_completa = web_p1 + serie_final + web_p2

    #buscamos la cantidad de episodios que tiene la serie
    web_ver = "https://monoschinos2.com/ver/" + serie_final
    resultado = requests.get(web_completa)
    content = resultado.text
    patron2 = fr'{web_ver}(.*)'

    while True:
        ep = input("Digite el número de episodio que desea ver (mayor o igual a 1 / 0 para salir): ")
        try:
            ep = int(ep)
            if ep >= 1:
                break
            elif ep == 0:
                return
            else:
                input("DIGITE UN NUMERO VÁLIDO")
        except:
            input("DIGITE UN NUMERO VÁLIDO")
    os.system("cls")
    print("por favor espere")
    while True:
        web_ep = web_ver + "-episodio-" + str(ep)
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver.get(web_ep)
        time.sleep(1) # espera a que la web cargue
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        break

    buscar_link = soup.find(id="videoLoading")
    web = "https://monoschinos2.com/reproductor"
    patron2 = fr'{web}(.*)'
    link_listo = re.findall(patron2, str(buscar_link)) 
    if link_listo == []:
        input("Lo lamento, el episodio no se encuentra disponible o no existe. Presione enter para volver ")
        return
    else:
        video = link_listo[0].split('"', maxsplit= 1)[0]
        link_video = web + video
        open(link_video)



#pagina 1 MONOS CHINOS
def pag1():
    serie = input("Serie a buscar: ")
    serie2 = serie.replace(" ", "+")
    website = "https://monoschinos2.com/buscar?q="
    website = website + serie2  #pagina con la serie a buscar
    resultado = requests.get(website)
    content = resultado.text
    
    patron = r'<h3 class="fs-6 text-light mt-2 title_cap">(.*)'#quiere decir que nos dará lo que hay despues de el texto (osea el titulo)
    titulos = re.findall(patron, str(content)) #buscamos los titulos en la pagina
    titulos_listos = []
    while True:
        os.system("cls")
        print("RESULTADOS PARA: ", serie, "\n")
        num = 1
        for i in titulos:
            nombre_titulo = i.replace("</h3>", "")
            titulos_listos.append((num, nombre_titulo))
            print(str(num) + ". ", nombre_titulo)
            num += 1 
        print("\n0. Salir\n")
        opcion = input("Digite una opción: ")
        match opcion:
            case "0":
                break
            case opcion if existe_titulo(opcion, titulos_listos) != False:
                #buscar anime
                abrir_link(existe_titulo(opcion, titulos_listos), str(content))
            case _:
                input("Digite una opcion correcta. <ENTER> ")
    return
#------------------------------------------------------------------
#FUNCION PRINCIPAL
#------------------------------------------------------------------
while True:
    os.system("cls")
    print("\n\n\n-------------------------------------------------------------------------------")
    print("                     ESCOJA UNA WEB\n")
    print("1. MonosChinos")
    print("0. Salir\n")
    opcion = input("Digite una opción: ")
    match opcion:
        case "1":
            pag1()
        case "0":
            break
        case _:
            input("Digite una opción correcta. <PRESIONE ENTER>")
