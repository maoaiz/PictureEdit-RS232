#!/usr/bin/python

#Programa para binarizar imagenes
#agradecimientos a Mariano Maccarrone.

#Modificado por: @MaoAiz - @JonathanMG7


import Image
import sys

img_fuente_default = "rojo.jpg"
img_salida_default = "img_binaria.bmp"
nombre_archivo_bin = "datos.txt" #aqui se almacenan los datos de la imagen en 1's y 0's

def main():
    if(len(sys.argv) > 1):
        img_fuente = sys.argv[1] # primer parametro   #
        print "Abriendo " + sys.argv[1]
    else:
        img_fuente = raw_input("ubicacion de la imagen:")#capturar por pantalla la ubicacion

    if(img_fuente != None):
        img_fuente = img_fuente_default
        
    archi=open(nombre_archivo_bin,'w')
    archi.close()

    im = Image.open(img_fuente)
    x,y = im.size
    print "\nimagen: %s \nsize:\tx: %d \ty: %d \n" % (img_fuente,x,y)
    
    datos = open(nombre_archivo_bin,"a")
    imageString = str(x)+","+str(y)+","
    for i in range(y):
            for j in range(x):
                    r,g,b = im.getpixel((j,i))
                    if  ((r+g+b)/3) < 125:
                            im.putpixel((j,i),(0,0,0))
                            datos.write("1")
                            imageString += "1"
                    else:
                            im.putpixel((j,i),(255,255,255))
                            datos.write("0")
                            imageString += "0"
            
            datos.write("\n")
            imageString += "."

    print "Revisa el archivo %s, ahi quedo toda la informacion" % (nombre_archivo_bin)
    
    datos.close()
    im.show()
    im.save(img_salida_default) 
    return imageString

main()