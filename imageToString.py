#!/usr/bin/python

#Programa para binarizar imagenes
#agradecimientos a Mariano Maccarrone.

#Modificado por: @MaoAiz - @JonathanMG7


import Image
import sys

img_fuente_default = "img/rojo.jpg"
img_salida_default = "img/img_binaria.bmp"
nombre_archivo_bin = "datos.txt" #aqui se almacenan los datos de la imagen en 1's y 0's

def codificarImg(img): #Recibe el string de la imagen modificada
	p=img.rsplit(',')
	x=p[0]
	y=p[1]
	pv=p[2].rsplit('.')
	print "imagen de: %s x %s \n"  % (x,y)
	try:
		size=int(x),int(y)
	
		im=Image.new('RGB', size)
				
		for i in range(int(y)):
			for j in range(int(x)):
				if pv[i][j]=="1":
					im.putpixel((j,i),(0,0,0)) #NO ESTA HACIENDO ESTO! SE VA SIEMPRE POR EL ELSE
				else:
					im.putpixel((j,i),(20,100,255))

		im.save("j.bmp") 

	except ValueError as details:
		
		print details
	
def main():
    if(len(sys.argv) > 1):
        img_fuente = sys.argv[1] # primer parametro   #
        print "Abriendo " + sys.argv[1]
    else:
        img_fuente = raw_input("ubicacion de la imagen:")#capturar por pantalla la ubicacion
        img_fuente = "img/"+img_fuente

    if(img_fuente != None or img_fuente != ""):
        img_fuente = img_fuente_default
        
    img_salida_default = img_fuente + ".bmp"
    
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

#main()
codificarImg("10,12,0000011111.0000011111.0000011111.0000011111.0000011111.0000011111.0000011111.0000011111.0000011111.0000011111.0000011111.0000011111.")
raw_input("")