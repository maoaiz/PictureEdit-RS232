#!/usr/bin/python

#Programa para binarizar imagenes
#agradecimientos a Mariano Maccarrone.

#Adaptado para binarizar imagenes y enviarlas por el puerto serie por: 
#                    @MaoAiz - @JonathanMG7


import Image
import sys
import serial
import threading

img_fuente_default = "img/rojo.jpg"
img_salida_default = "img/img_binaria.bmp"
nombre_archivo_bin = "datos.txt" #aqui se almacenan los datos de la imagen en 1's y 0's
EXITCHARCTER = 'exit'   #ctrl+D  #-- Caracter empleado para salir del terminarl
global fin                          #-- Variable para indicar al thread que termine
global s
global r
Port=0
global data

try:
		s = serial.Serial(Port, 115200)
		s.timeout=1;
except serial.SerialException:
		sys.stderr.write("Error al abrir puerto: " + str(Port)+"\n")
		sys.exit(1)

print ("Puerto serie (%s): %s") % (str(Port),s.portstr)

def reader():
	'''
	 Este thread se ejecuta infinitamente. Esta todo el rato leyendo datos
	 del puerto serie
	'''
	fin = 0
	data = ""
	#-- Cuando fin=1 se termina el thread
	while not(fin):
		try:
			data += s.read()
			#print "%s" % (data)
			#enviar data a decodificar
			if len(data) > 1:
				if data[len(data)-1]=="q":
					codificarImg(data[0:-1])
					data = ""
		except serial.SerialException:
			print "Excepcion: Abortando..."
			break;     
			
	print "data: %s" % data
	
	
def writer():
	img_bin = binarizar()+"q"
	print "La Imagen se binarizo con exito.\n"
	while 1:
		try:          #img_bin = binarizar()   #string de la imagen binarizada            #-- Si es la tecla de fin se termina
			op = 	raw_input("Desea enviar la imagen por el puerto serie?(y/n/exit):")
			if op == EXITCHARCTER:
				fin = 1
				break
			else:
				#-- Enviar tecla por el puerto serie
				if op == "y":
					s.write(img_bin)
					print "\nenviado:\n" 
				else:
					if op == "n":
						writer()
					else:
						print "\n----------------Ingresa una opcion valida----------------\n"
						
		except ValueError as e: #-- Si se ha pulsado control-c terminar
			print "Excep Abortando: %s \n" % (e)
			break
		except:
			print "\nError al enviar!\n"
			break

def binarizar():
    '''
    captura una imagen y la binariza.
    retorna un string con los datos de la imagen binarizada incluyendo ancho y alto
    en el siguiente formato:
        ancho,alto,fila1.fila2.fila3 donde cada fila son la secuencia de los pixeles de la imagen
        1 = representa color negro
        0 = representa color blanco 
        ej: 10,2,1111111111.10000000001 
        esto seria una img de 10x2
        la fila 1 esta pintada y la fila 2 solo esta pintada en el primer y ultimo pixel
        
    Esta funcion lee el primer argumento pasado por consola
        ej: $ python imageToString.py miImagen.jpg 
    
    '''
    #capturar imagen desde argumentos del sistema o desde consola
    if(len(sys.argv) > 1):
        img_fuente = sys.argv[1] # primer parametro   #
        print "Abriendo " + sys.argv[1]
    else:
        img_fuente = raw_input("ubicacion de la imagen:")#capturar por pantalla la ubicacion

    if(img_fuente == None or img_fuente == ""):
        img_fuente = img_fuente_default
        
    img_salida_default = img_fuente + ".bmp" # esta linea se puede mejorar (quitar la extension inicial de la imagen)
    
    #crear archivo para guardar datos binarios de la imagen
    archi=open(nombre_archivo_bin,'w')
    archi.close()

    #abrir imagen para recorrer
    im = Image.open(img_fuente)
    x,y = im.size
    print "\nimagen: %s \nsize:\tx: %d \ty: %d \n" % (img_fuente,x,y)
    
    #guardar datos en el archivo
    datos = open(nombre_archivo_bin,"a")
    imageString = str(x)+","+str(y)+","
    #recorrer la imagen
    for i in range(y):
            for j in range(x):
                    r,g,b = im.getpixel((j,i))
                    if  ((r+g+b)/3) < 125:
                            im.putpixel((j,i),(0,0,0))  #crear nueva imagen
                            datos.write("1")            #guardar en datos
                            imageString += "1"          #crear string de la imagen
                    else:
                            im.putpixel((j,i),(255,255,255))
                            datos.write("0")
                            imageString += "0"
            
            datos.write("\n")
            imageString += "."

    print "Revisa el archivo %s, ahi quedo toda la informacion\n" % (nombre_archivo_bin)
    datos.close()               #cierra el archivo con los datos
    im.save(img_salida_default) #guarda la imagen binarizada 
    #im.show()                   #muestra la nueva imagen binarizada
    return imageString          #retorna un string con los datos de la imagen 

def codificarImg(img): #Recibe el string de la imagen modificada
	print "\n"
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
					im.putpixel((j,i),(255,255,255))
	
		im.save("img/recibido/newImage.bmp")
		im.show() 
	
	except ValueError as details:
		
		print details


def main():
	Port = 0
	r = threading.Thread(target=reader) #-- Lanzar el hilo que lee del puerto serie y saca por pantalla
	r.start()
	writer()                            #enviar imagen por puerto serie RS232
	fin=1
	#-- Fin del programa
	print "\n\n--- Fin ---"
	r.join()
	s.close()

main()
