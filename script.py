import sqlite3 as sql
import serial
import time

arduino = serial.Serial('/dev/ttyACM0', 9600)


while True:
	c = 0
	suma_pulso = 0
	while c < 6: 
		pulso_ps = int(arduino.readline())
		temperatura = float(arduino.readline())
		suma_pulso = suma_pulso + pulso_ps
		c = c + 1
		time.sleep(1)
	print("despues del while")
	promedio_pulso = suma_pulso / 5
	info =  [promedio_pulso, temperatura]
	print(info)
	with sql.connect("base_datos.db") as con: #Conectamos a la base de datos y lo llamamos "con"
		print("antes del try")
		try:
			cursor = con.cursor()
			cursor.execute('''CREATE TABLE IF NOT EXISTS dbsensores (
								pulso number,
								temperatura number
								);'''
							)
			cursor.execute('''INSERT INTO dbsensores (pulso, temperatura) VALUES (?,?);''', info)
			con.commit()
		except Exception as e:
			print(str(e))
