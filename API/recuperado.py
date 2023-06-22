from datetime import date
from sqlite3 import *
from tkinter import *
from tkinter import messagebox

            
class Datos ():
	def __init__(self, path):

		self.conexion = connect("DB.db")


		self.conexion.row_factory = Row
 
		self.cursor = self.conexion.cursor()
		self.iniciar()


	def execute(self, query, *parametros):
		self.cursor.execute(query, (*parametros,))
		self.conexion.commit() # No se si está bien el commit cada ejecución pero fue
		return self.cursor.fetchall()

	def executemany(self, query, lista):
		self.cursor.executemany(query, lista)
		self.conexion.commit() # No se si está bien el commit cada ejecución pero fue
		return self.cursor.fetchall()

	def actualizar(self):
		self.execute("DELETE FROM Consumos")

		datos_lotes = self.execute("SELECT * FROM Lotes")
		datos_props = self.execute("SELECT * FROM propietarios")
		datos_costos = self.execute("SELECT * FROM costos")

		pago_lot = []
		pago_man = []
		pago_nombre = []
		pago_seguridad = []
		pago_luz = []
		pago_agua = []
		pago_gas = []
		pago_luz_publica = []
		pago_f_agua = []
		pago_f_asf = []
		pago_vehiculo = []
		valor_terreno = []




		lotes_construidos = 0
		for row in datos_props:
			if row["sup_cub"] > 0:
				lotes_construidos += 1

		lotes_luz = 0
		for row in datos_lotes:
			if row["luz"]:
				lotes_luz += 1

		pago_lote_const = datos_costos[0]["seguridad"] / (len(datos_props) + lotes_construidos)
		pago_lote_no_const = pago_lote_const * 2

		for i in range(len(datos_props)):
			pago_lot.append(datos_props[i]["lote"])
			pago_man.append(datos_props[i]["manzana"])
			pago_nombre.append(
				datos_props[i]["nomape"])

			if datos_props[i]["sup_cub"] > 0:
				pago_seguridad.append(pago_lote_const)
			else:
				pago_seguridad.append(pago_lote_no_const)

			pago_luz.append(
				datos_costos[0]["kw"] * datos_props[i]["cons_luz"])
			pago_agua.append(
				datos_costos[0]["m3_agua"] * datos_props[i]["cons_agua"])
			pago_gas.append(
				datos_costos[0]["m3_gas"] * datos_props[i]["cons_gas"])

			luz = esq = False
			lote_f = lote_p = 0

			for j in range(len(datos_lotes)):
				if datos_lotes[j]["numero"] == datos_props[i]["lote"] and datos_lotes[j]["manzana"] == datos_props[i]["manzana"]:
					luz = datos_lotes[j]["luz"]
					esq = datos_lotes[j]["esq"]
					lote_f = datos_lotes[j]["m_frente"]
					lote_p = datos_lotes[j]["m_prof"]
			if luz:
				pago_luz_publica.append(
					datos_costos[0]["total_luz"] / lotes_luz)
			else:
				pago_luz_publica.append(0)

			if esq:
				pago_f_agua.append(
					datos_costos[0]["mf_agua"] * (lote_f + lote_p))
				pago_f_asf.append(
					datos_costos[0]["mf_asf"] * (lote_f + lote_p))
			else:
				pago_f_agua.append(
					datos_costos[0]["mf_agua"] * (lote_p))
				pago_f_asf.append(
					datos_costos[0]["mf_asf"] * (lote_p))

			pago_vehiculo.append(
				datos_costos[0]["vehiculos"] * datos_props[i]["vehiculos"])
			valor_terreno.append(
				(lote_f * lote_p) * datos_costos[0]["m2_valor"])

		lista = [pago_lot, pago_man, pago_nombre, pago_seguridad, pago_luz, pago_agua, pago_gas, pago_luz_publica, pago_f_agua, pago_f_asf, pago_vehiculo, valor_terreno]
		transpuesta = []

		for i in range(len(lista[0])):
			f = []
			for j in range(len(lista)):
				f.append(lista[j][i])
			transpuesta.append(f)

		self.cursor.executemany("INSERT INTO Consumos Values (?,?,?,?,?,?,?,?,?,?,?,?)", transpuesta)


	def iniciar(self):
		self.cursor.execute("CREATE TABLE IF NOT EXISTS Costos (seguridad, kw INTEGER, m3_agua INTEGER, m3_gas INTEGER, total_luz INTEGER, mf_agua INTEGER, mf_asf INTEGER, vehiculos INTEGER, m2_valor INTEGER)")
		self.cursor.execute("CREATE TABLE IF NOT EXISTS Consumos (lot INTEGER, man INTEGER, nombre VARCHAR, seguridad FLOAT, luz FLOAT, agua FLOAT, gas FLOAT, luz_publica FLOAT, f_agua FLOAT, f_asf FLOAT, vehiculo FLOAT, terreno FLOAT)")
		self.cursor.execute("CREATE TABLE IF NOT EXISTS Propietarios (nomape VARCHAR, lote INTEGER, manzana INTEGER, fecha INTEGER, sup_cub INTEGER, habitantes INTEGER, vehiculos INTEGER, cons_luz INTEGER, cons_agua INTEGER, cons_gas INTEGER)")
		self.cursor.execute("CREATE TABLE IF NOT EXISTS Lotes (numero INTEGER, manzana INTEGER, m_frente INTEGER, m_prof INTEGER, luz INTEGER, agua INTEGER, asf INTEGER, esq INTEGER, lote_id INTEGER)")

		self.cursor.execute("SELECT * FROM Costos")
		if self.cursor.fetchall() == []:
			self.execute("INSERT INTO Costos VALUES (?,?,?,?,?,?,?,?,?)", 30000, 60, 30, 45, 80000, 40, 70, 10000, 60000)

		prop_data = [["Perez Luis",1,1,20160922,600,2,1,0,2400,1500],
		["Perez Luis",2,1,20160922,830,0,0,1100,0,0],
		["Martinez Marcos",1,2,20181204,230,4,2,1200,200,2300],
		["Gomez Lucas",1,3,20220431,0,0,0,0,1400,0],
		["Perez Luis",2,2,20210212,0,0,0,0,0,0],
		["Perez Luis",2,3,20200512,700,5,3,0,4230,3400]]







		self.cursor.execute("SELECT * FROM Propietarios")
		if self.cursor.fetchall() == []:
			self.executemany("INSERT INTO Propietarios VALUES (?,?,?,?,?,?,?,?,?,?)", prop_data)



		lote_data = [[1,1,100,120,0,1,1,1,1],
		[2,1,110,90,1,0,1,0,2],
		[1,2,90,110,1,1,0,1,3],
		[2,2,110,100,0,1,0,0,4],
		[1,3,85,100,0,0,1,1,5],
		[2,3,100,85,0,1,1,0,6],
		[1,4,100,120,1,1,2,2,7]]



		self.cursor.execute("SELECT * FROM Lotes")
		if self.cursor.fetchall() == []:
			self.executemany("INSERT INTO Lotes VALUES (?,?,?,?,?,?,?,?,?)", lote_data)




class Menu ():

	def __init__(self, titulo):
		self.frame = CrearFrame(raiz, h=768)
		self.frame.grid_columnconfigure(0, weight=1)
		self.frame.grid_columnconfigure(1, weight=1)
		self.frame.grid_rowconfigure(12, weight=1)
		self.frame.grid_rowconfigure(13, weight=1)  # ROW ATras
		self.titulo = CrearLabel(self.frame, titulo, 20)

		self.f = False

	def mostrar(self):
		Gridear(self.frame, 1, 0, cs=2)

	def esconder(self):
		self.frame.grid_forget()

	def volver(self, donde):
		self.frame.grid_forget()
		donde.mostrar()





class Principal(Menu):

	def __init__(self, textos, iconos):
		super().__init__("Principal")

		self.frame.grid_rowconfigure(2, weight=1)
		self.frame.grid_rowconfigure(3, weight=1)

		self.botones = []
		for i in range(4):
			self.botones.append(CrearButton(self.frame, text=textos[i],
											image=iconos[i], compound=TOP, width=50, height=400))

	def setearComandos(self, comandos):
		for i in range(4):
			self.botones[i].config(command=comandos[i])

	def a(self, donde):
		self.esconder()
		donde.mostrar()

	def mostrar(self):
		Gridear(self.frame, 1, 0, cs=2)
		if not self.f:

			self.f = True
			Gridear(self.titulo, 1, 0, cs=2, py=(20, 0))

			Gridear(self.botones[0], 2, 0, px=20, py=20)
			Gridear(self.botones[1], 2, 1, px=20, py=20)
			Gridear(self.botones[2], 3, 0, px=20, py=20)
			Gridear(self.botones[3], 3, 1, px=20, py=20)


class Lotes(Menu):
	def __init__(self, titulo, principal, datos):
		super().__init__(titulo)
		self.principal = principal
		self.datos = datos

		self.boton_atras = boton_atras(
			self.frame, lambda: self.volver(self.principal), ico=ArrowBackIcon)

		self.boton_confirmar = CrearButton(self.frame, image=SaveIcon, command=self.guardar, text="Guardar datos  ",
										   compound=RIGHT, width=300)

		l0 = CrearLabel(self.frame, "N° de lote: ",
						anchor="w", altoLetra=20,)
		l2 = CrearLabel(self.frame, "N° de manzana: ",
						anchor="w", altoLetra=20,)
		l3 = CrearLabel(self.frame, "M. de frente: ",
						anchor="w", altoLetra=20,)
		l4 = CrearLabel(self.frame, "M. de profundidad: ",
						anchor="w", altoLetra=20,)
		l5 = CrearLabel(self.frame, "Alumbrado público: ",
						anchor="w", altoLetra=20,)
		l6 = CrearLabel(self.frame, "Agua pública: ",
						anchor="w", altoLetra=20,)
		l7 = CrearLabel(self.frame, "Calle asfaltada: ",
						anchor="w", altoLetra=20,)
		l8 = CrearLabel(self.frame, "En la esquina: ",
						anchor="w", altoLetra=20,)

		self.labels = [l0, l2, l3, l4, l5, l6, l7, l8]

		e0 = CrearEntry(
			self.frame, color["fondo"], color["letra"], 20, LEFT, width=10)
		e1 = CrearEntry(
			self.frame, color["fondo"], color["letra"], 20, LEFT, width=10)
		e2 = CrearEntry(
			self.frame, color["fondo"], color["letra"], 20, LEFT, width=10)
		e3 = CrearEntry(
			self.frame, color["fondo"], color["letra"], 20, LEFT, width=10)

		self.var1 = IntVar()
		self.var2 = IntVar()
		self.var3 = IntVar()
		self.var4 = IntVar()

		c0 = CrearRadios(self.frame, self.var1, "Si", "No")
		c1 = CrearRadios(self.frame, self.var2, "Si", "No")
		c2 = CrearRadios(self.frame, self.var3, "Si", "No")
		c3 = CrearRadios(self.frame, self.var4, "Si", "No")

		self.entries = [e0, e1, e2, e3]
		self.radios = [c0, c1, c2, c3]

	def mostrar(self):
		try:
			self.principal.esconder()
		except:
		  #  print("EL except salto")
			pass

		Gridear(self.frame, 1, 0, cs=2)

		if not self.f:

			self.f = True
			Gridear(self.titulo, 1, 0, cs=3, py=(20, 0))

			for i in range(len(self.labels)):
				Gridear(self.labels[i], i+2, 0, py=5, px=5)

			for i in range(len(self.entries)):
				Gridear(self.entries[i], i+2, 1, cs=2, py=5, px=5)

			for i in range(len(self.radios)):
				for j in range(len(self.radios[i])):
					Gridear(self.radios[i][j], i+6, j+1)

			Gridear(self.boton_confirmar, 12, 0, cs=3, py=(20, 0), sticky="")
			Gridear(self.boton_atras, 13, 0, cs=2, sticky="sw", py=20, px=20)

	def guardar(self):
	   # print("Validando...")
		v = True

		msj = ""

		lote_numero = self.entries[0].get()
		if lote_numero == "":
			msj += "Faltó ingresar el número de lote\n"
			v = False

		lote_manzana = self.entries[1].get()
		if lote_manzana == "":
			msj += "Faltó ingresar el número de manzana\n"
			v = False

		lote_frente_m = self.entries[2].get()
		if lote_frente_m == "":
			msj += "Faltó ingresar los metros de frente\n"
			v = False

		lote_prof_m = self.entries[3].get()
		if lote_prof_m == "":
			msj += "Faltó ingresar los metros de profundidad\n"
			v = False

		lote_luz = self.var1.get()
		if lote_luz == 0 or lote_luz == "" or lote_luz == "0":
			msj += "Faltó seleccionar si tiene luz\n"
			v = False

		lote_agua = self.var2.get()
		if lote_agua == 0 or lote_agua == "" or lote_agua == "0":
			msj += "Faltó seleccionar si tiene agua\n"
			v = False

		lote_asf = self.var3.get()
		if lote_asf == 0 or lote_asf == "" or lote_asf == "0":
			msj += "Faltó seleccionar si tiene asfalto\n"
			v = False

		lote_esq = self.var4.get()
		if lote_esq == 0 or lote_esq == "" or lote_esq == "0":
			msj += "Faltó seleccionar si está en la esquina\n"
			v = False

		try:
			lote_numero = int(lote_numero)
		except:
			v = False
			msj += "El lote debe ser un número entero\n"
			self.entries[0].delete(0, END)

		else:
			if lote_numero < 1:
				msj += "El lote debe ser positivo\n"
				v = False

		try:
			lote_manzana = int(lote_manzana)
		except:
			v = False
			msj += "La manzana debe ser un número entero\n"
			self.entries[1].delete(0, END)

		else:
			if lote_manzana < 1:
				v = False
				msj += "La manzana debe ser positiva\n"

		numeros = self.datos.execute("SELECT numero FROM LOTES")
		numeros = [i["numero"] for i in numeros]

		manzanas = self.datos.execute("SELECT manzana FROM LOTES")
		manzanas = [i["manzana"] for i in manzanas]

		if v:
			if not len(numeros) == len(manzanas): print("Los len son desiguales y algo salió mal")
			for i in range(len(manzanas)):
				if numeros[i] == lote_numero and manzanas[i] == lote_manzana:
					self.entries[0].delete(0, END)
					self.entries[1].delete(0, END)
					v = False
					msj += "El lote y la manzana ya están ingresados\n"
					break

		try:
			lote_frente_m = int(lote_frente_m)
		except:
			v = False
			msj += "Los metros de frente deben ser un número entero\n"
			self.entries[2].delete(0, END)

		else:
			if lote_frente_m < 1:
				msj += "Los metros de frente deben ser positivos\n"

		try:
			lote_prof_m = int(lote_prof_m)

		except:
			v = False
			msj += "Los metros de profundidad deben ser un número entero\n"
			self.entries[3].delete(0, END)

		else:
			if lote_prof_m < 1:
				msj += "Los metros de profundidad deben ser positivos\n"

		if v:

			messagebox.showinfo("Bien ahí!", "Datos cargados correctamente")

			self.datos.execute(f"INSERT INTO Lotes (numero, manzana, m_frente, m_prof, luz, agua, asf, esq) VALUES({lote_numero},{lote_manzana},{lote_frente_m},{lote_prof_m},{lote_luz},{lote_agua},{lote_asf},{lote_esq})")




			for i in self.entries:
				i.delete(0, END)

			self.var1.set(0)
			self.var2.set(0)
			self.var3.set(0)
			self.var4.set(0)


		else:
			messagebox.showerror("Error al cargar", msj)
		# for i in self.datos.datos_lotes:
			# print(self.datos.datos_lotes[i])


class Propietarios(Menu):
	def __init__(self, titulo, principal, datos):
		super().__init__(titulo)
		self.principal = principal
		self.datos = datos
		self.boton_atras = boton_atras(
			self.frame, lambda: self.volver(self.principal), ico=ArrowBackIcon)
		self.boton_confirmar = CrearButton(self.frame, image=SaveIcon, command=self.guardar, text="Guardar datos  ",
										   compound=RIGHT, width=300)

		na = CrearLabel(self.frame, "Nombre y apellido",
						altoLetra=17, anchor="w")
		l = CrearLabel(self.frame, "N° de lote", altoLetra=17, anchor="w")
		m = CrearLabel(self.frame, "N° de manzana", altoLetra=17, anchor="w")
		f = CrearLabel(self.frame, "Fecha de compra", altoLetra=17, anchor="w")
		m2 = CrearLabel(self.frame, "Metros cubiertos",
						altoLetra=17, anchor="w")
		h = CrearLabel(self.frame, "Habitantes", altoLetra=17, anchor="w")
		v = CrearLabel(self.frame, "Vehículos", altoLetra=17, anchor="w")
		cl = CrearLabel(self.frame, "Consumo de luz", altoLetra=17, anchor="w")
		ca = CrearLabel(self.frame, "Consumo de agua",
						altoLetra=17, anchor="w")
		cg = CrearLabel(self.frame, "Consumo de gas", altoLetra=17, anchor="w")

		e_na = CrearEntry(self.frame, width=10, altoLetra=17)
		e_l = CrearEntry(self.frame, width=10, altoLetra=17)
		e_m = CrearEntry(self.frame, width=10, altoLetra=17)
		#e_f = CrearEntry(self.frame, width = 10, altoLetra=17)
		e_m2 = CrearEntry(self.frame, width=10, altoLetra=17)
		e_h = CrearEntry(self.frame, width=10, altoLetra=17)
		e_v = CrearEntry(self.frame, width=10, altoLetra=17)
		e_cl = CrearEntry(self.frame, width=10, altoLetra=17)
		e_ca = CrearEntry(self.frame, width=10, altoLetra=17)
		e_cg = CrearEntry(self.frame, width=10, altoLetra=17)

		self.labels = [na, l, m, f, m2, h, v, cl, ca, cg]
		self.entries = [e_na, e_l, e_m,  e_m2,
						e_h, e_v, e_cl, e_ca, e_cg]  # e_f,

		self.calendario = DateEntry(self.frame, selectmode="day", font=fuente(
			17), background=color["acento"], foreground=color["letra"])

	def mostrar(self):
		try:
			self.principal.esconder()
		except:
	  #     print("Algo tiró un error, mostrar propietarios")
			pass

		Gridear(self.frame, 1, 0, cs=2)

		if not self.f:

			self.f = True
			Gridear(self.titulo, 1, 0, cs=2, py=(20, 14))

			for i in range(len(self.labels)):
				Gridear(self.labels[i], i+2, 0, py=3, px=7)

			for i in range(len(self.entries)):
				if i == 3:
					Gridear(self.calendario, 5, 1, py=3, px=7)
				else:
					Gridear(self.entries[i], i+2, 1, py=3, px=7)
				if i > 2:
					Gridear(self.entries[i], i+3, 1, py=3, px=7)

			Gridear(self.boton_confirmar, 12, 0, cs=2, py=(20, 0), sticky="")
			Gridear(self.boton_atras, 13, 0, cs=2, sticky="sw", py=20, px=20)

	def guardar(self):
		v = True

		msj = ""

		nomape = self.entries[0].get()
		if not nomape.strip().isalpha():
			v = False
			msj += "El nombre debe ser un nombre\n"
			self.entries[0].delete(0, END)

		try:
			lote = int(self.entries[1].get())
		except:
			v = False
			msj += "El lote debe ser un número entero\n"
			self.entries[1].delete(0, END)

		else:
			if not lote > 0:
				v = False
				msj += "El lote debe ser positivo\n"

		try:
			manzana = int(self.entries[2].get())
		except:
			v = False
			msj += "La manzana debe ser un número entero\n"
			self.entries[2].delete(0, END)

		else:
			if not manzana > 0:
				v = False
				msj += "La manzana debe ser positiva\n"

		numeros = self.datos.execute("SELECT lote FROM PROPIETARIOS")
		numeros = [i["lote"] for i in numeros]

		manzanas = self.datos.execute("SELECT manzana FROM PROPIETARIOS")
		manzanas = [i["manzana"] for i in manzanas]

		if v:
			if not len(manzanas) == len(numeros): print("Los len de las listasa no son iguales, mal ahí")
			for i in range(len(manzanas)):
				if numeros[i] == lote and manzanas[i] == manzana:
					self.entries[1].delete(0, END)
					self.entries[2].delete(0, END)
					v = False
					msj += "El lote y la manzana ya están ingresados\n"
					break

			f = False

			numeros = self.datos.execute("SELECT numero FROM LOTES")
			numeros = [i["numero"] for i in numeros]

			manzanas = self.datos.execute("SELECT manzana FROM LOTES")
			manzanas = [i["manzana"] for i in manzanas]



			for i in range(len(manzanas)):
				if numeros[i] == lote and manzanas[i] == manzana:
					f = True

			if not f:
				v = False
				self.entries[1].delete(0, END)
				self.entries[2].delete(0, END)
				msj += "El lote y manzana seleccionados no están cargados\n"


		fecha = self.calendario.get_date()

		try:
			sup = int(self.entries[3].get())
		except:
			v = False
			msj += "La superficie debe ser un número entero\n"
			self.entries[3].delete(0, END)

		else:
			if not sup >= 0:
				v = False
				msj += "La superficie debe ser positiva\n"
		try:
			habitantes = int(self.entries[4].get())
		except:
			v = False
			msj += "Los habitantes deben ser un número entero\n"
			self.entries[4].delete(0, END)

		else:
			if not habitantes >= 0:
				v = False
				msj += "Los habitantes deben ser positivos\n"
		try:
			vehiculos = int(self.entries[5].get())
		except:
			v = False
			msj += "Los vehículos deben ser un número entero\n"
			self.entries[5].delete(0, END)

		else:
			if not vehiculos >= 0:
				v = False
				msj += "Los vehículos deben ser positivos\n"
		try:
			luz = int(self.entries[6].get())
		except:
			v = False
			msj += "La luz debe ser un número entero\n"
			self.entries[6].delete(0, END)

		else:
			if not luz >= 0:
				v = False
				msj += "la luz debe ser positiva\n"
		try:
			agua = int(self.entries[7].get())
		except:
			v = False
			msj += "El agua debe ser un número entero\n"
			self.entries[7].delete(0, END)

		else:
			if not agua >= 0:
				v = False
				msj += "El agua debe ser positiva\n"
		try:
			gas = int(self.entries[8].get())
		except:
			v = False
			msj += "El gas debe ser un número entero"
			self.entries[8].delete(0, END)

		else:
			if not gas >= 0:
				v = False
				msj += "El gas debe ser positivo\n"

		if v:
			messagebox.showinfo("Bien ahí!", "Datos cargados correctamente")

			self.datos.execute(f"INSERT INTO PROPIETARIOS VALUES (?,?,?,?,?,?,?,?,?,?)", nomape, lote, manzana, fecha, sup, habitantes, vehiculos, luz, agua, gas)


			for i in self.entries:
				i.delete(0, END)

			self.datos.actualizar()
		else:
			messagebox.showerror("Error", msj)

		# for i in self.datos.datos_props:
			# print(self.datos.datos_props[i])


class Consultas(Menu):
	def __init__(self, titulo, principal, datos):
		super().__init__(titulo)
		self.principal = principal
		self.datos = datos
		self.boton_atras = boton_atras(
			self.frame, lambda: self.volver(self.principal), ico=ArrowBackIcon)

		#self.frame.grid_rowconfigure(2, weight = 1)

		self.frame_lotes = CrearFrame(self.frame, bg=color["contraste"])
		self.frame_props = CrearFrame(self.frame, bg=color["contraste"])

		self.boton_lotes = CrearButton(
			self.frame, bg=color["acento"], text="Lotes",	command=lambda: self.mostrar_lotes(), height=2)
		self.boton_props = CrearButton(
			self.frame, bg=color["acento"], text="Propietarios ", command=lambda: self.mostrar_props(), height=2)

		# por lotes
		self.l_var_m = StringVar()
		self.l_var_m.set("Manzana")
		self.l_var_l = StringVar()
		self.l_var_l.set("Lote")

		l_ms = []
		l_ls = []

		numeros = self.datos.execute("SELECT numero FROM LOTES")
		numeros = [i["numero"] for i in numeros]

		manzanas = self.datos.execute("SELECT manzana FROM LOTES")
		manzanas = [i["manzana"] for i in manzanas]



		for manzana in manzanas:

			if manzana not in l_ms:
				l_ms.append(manzana)

		for numero in numeros:
			if numero not in l_ls:
				l_ls.append(numero)

		l_ms.append("Manzana")
		l_ls.append("Lote")

		self.l_menu_manz = CrearMenu(
			self.frame_lotes, self.l_var_m, l_ms, comando=self.func_lotes, width=10)
		self.l_menu_lote = CrearMenu(
			self.frame_lotes, self.l_var_l, l_ls, comando=self.func_lotes, width=10)

		self.l_frame_muestra = CrearFrame(
			self.frame_lotes, bg=color["contraste"])
		self.l_scrollbar = Scrollbar(self.frame_lotes)
		self.l_listbox = CrearListbox(self.l_frame_muestra)

		self.l_listbox.config(yscrollcommand=self.l_scrollbar.set)
		self.l_scrollbar.config(command=self.l_listbox.yview)
		# por manzana
		# por lote y manzana

		# por propietarios
		self.p_var_m = StringVar()
		self.p_var_m.set("Manzana")
		self.p_var_l = StringVar()
		self.p_var_l.set("Lote")
		self.p_var_na = StringVar()
		self.p_var_na.set("Nombre")

		p_ms = []
		p_ls = []
		p_ns = []

		manzanas = self.datos.execute("SELECT manzana FROM PROPIETARIOS")
		lotes = self.datos.execute("SELECT lote FROM PROPIETARIOS")
		nomapes = self.datos.execute("SELECT nomape FROM PROPIETARIOS")


		manzanas = [i["manzana"] for i in manzanas]
		lotes = [i["lote"] for i in lotes]
		nomapes = [i["nomape"] for i in nomapes]


		for manzana in manzanas:
			if manzana not in p_ms:
				p_ms.append(manzana)


		for lote in lotes:
			if lote not in p_ls:
				p_ls.append(lote)

		for nomape in nomapes:
			if nomape not in p_ns:
				p_ns.append(nomape)

		p_ms.append("Manzana")
		p_ls.append("Lote")
		p_ns.append("Nombre")

		self.p_menu_manz = CrearMenu(
			self.frame_props, self.p_var_m, p_ms, comando=self.func_props, width=6)


		self.p_menu_lote = CrearMenu(
			self.frame_props, self.p_var_l, p_ls, comando=self.func_props, width=6)

		self.p_menu_nomb = CrearMenu(
			self.frame_props, self.p_var_na, p_ns, comando=self.func_props, width=6)

		self.p_frame_muestra = CrearFrame(
			self.frame_props, bg=color["contraste"])
		self.p_scrollbar = Scrollbar(self.frame_props)
		self.p_listbox = CrearListbox(self.p_frame_muestra)
		self.p_listbox.config(yscrollcommand=self.p_scrollbar.set)
		self.p_scrollbar.config(command=self.p_listbox.yview)

		# por apellido
		# por manzana
		# por lote y manzana

		self.mostrar_lotes()
		self.func_lotes(None)
		self.func_props(None)

	def func_lotes(self, _algo):
		self.l_listbox.delete(0, END)

		m = self.l_var_m.get()
		try:
			m = int(m)
		except:
			pass

		l = self.l_var_l.get()
		try:
			l = int(l)
		except:
			pass

		linea = 0

		datos = self.datos.execute("SELECT * FROM LOTES")




		for i in range(len(datos)):

			if m != "Manzana":
				if m != datos[i][1]:
					continue

			if l != "Lote":
				if l != datos[i][0]:
					continue

			string = ["Viendo lote {} manzana {}".format(datos[i][0], datos[i][1], ),
					  "Frente {}m, Profundidad: {}m".format(
						  datos[i][2], datos[i][3],),
					  "Luz: {}, Agua: {}".format(si_no(datos[i][4]), si_no(
						  datos[i][5]),),
					  "Esquina: {}, Asfalto: {}".format(si_no(datos[i][6]), si_no(
						  datos[i][7])),
					  "",
					  "-"*32,
					  "", ]

			for j in range(len(string)):
				self.l_listbox.insert(linea, string[j])
				linea += 1

	def func_props(self, algo):
		self.p_listbox.delete(0, END)

		m = self.p_var_m.get()
		try:
			m = int(m)
		except:
			pass

		l = self.p_var_l.get()
		try:
			l = int(l)
		except:
			pass

		n = self.p_var_na.get()

		linea = 0

		datos = self.datos.execute("SELECT * FROM PROPIETARIOS")

		for i in range(len(datos)):

			if m != "Manzana":
				if m != datos[i][2]:
					continue

			if l != "Lote":
				if l != datos[i][1]:
					continue

			if n != "Nombre":
				if n != datos[i][0]:
					continue

			string = ["{}".format(datos[i][0]),
					  "Lote: {}, manzana: {}".format(
						  datos[i][1], datos[i][2]),
					  "Fecha de compra: {}".format(
				datos[i][3]),
				"Metros cubiertos: {}m2".format(
			   datos[i][4]),
				"Habitantes: {}".format(
			   datos[i][5]),
				"Vehículos: {}".format(
			   datos[i][6]),
				"Consumo de luz: {}".format(
			   datos[i][7]),
				"Consumo de agua: {}".format(
			   datos[i][8]),
				"Consumo de gas: {}".format(
			   datos[i][9]),
				"",
				"-"*32,
				"", ]
			for i in range(len(string)):
				self.p_listbox.insert(linea, string[i])
				linea += 1

	def mostrar(self):

		self.cambiar_menues()
		self.func_lotes(None)

		try:
			self.principal.esconder()
		except:
			pass  # TODO: hace falta?

		Gridear(self.frame, 1, 0, cs=2)

		if not self.f:

			self.f = True
			Gridear(self.titulo, 1, 0, cs=2, py=(20, 8))

			Gridear(self.boton_lotes, 2, 0, sticky="", px=(6, 3), py=6)
			Gridear(self.boton_props, 2, 1, sticky="",
					px=(3, 6), py=6)

			Gridear(self.boton_atras, 13, 0, cs=2, sticky="sw", py=20, px=20)

	def mostrar_lotes(self):
		self.frame_props.grid_forget()
		Gridear(self.frame_lotes, 3, 0, cs=2)
		Gridear(self.l_menu_manz, 0, 0, py=5, px=10, sticky="ew")
		Gridear(self.l_menu_lote, 0, 1, py=5, px=10, cs=2, sticky="ew")
		Gridear(self.l_frame_muestra, 1, 0, cs=2, px=5)
		Gridear(self.l_scrollbar, 1, 1, cs=1, sticky="nse", px=5)
		Gridear(self.l_listbox, 1, 0, cs=2)

	def mostrar_props(self):
		self.frame_lotes.grid_forget()
		Gridear(self.frame_props, 3, 0, cs=3)
		Gridear(self.p_menu_manz, 0, 0, py=5, px=(10, 5), sticky="ew")
		Gridear(self.p_menu_lote, 0, 1, py=5, px=(5, 5), sticky="ew")
		Gridear(self.p_menu_nomb, 0, 2, py=5, px=(5, 10), sticky="ew")

		Gridear(self.p_frame_muestra, 1, 0, cs=3, px=5)
		Gridear(self.p_scrollbar, 1, 2, cs=1, sticky="nse", px=5)
		Gridear(self.p_listbox, 1, 0, cs=2)

	def cambiar_menues(self):
		m = []
		l = []

   #     print("Cambiando menues")

		datos = self.datos.execute("SELECT * FROM LOTES")

		manzanas = self.datos.execute("SELECT manzana FROM LOTES")
		lotes = self.datos.execute("SELECT numero FROM LOTES")
		manzanas = [i["manzana"] for i in manzanas]
		lotes = [i["numero"] for i in lotes]

		for manzana in manzanas:

			# print(self.datos.datos_lotes["lote_manzana"][i], "de la db")
			if manzana not in m:
				m.append(manzana)

		for lote in lotes:
			if lote not in l:
				l.append(lote)
	   # print("llamamos con ", m)
		self.cambiar_lotes(m, l)

		m = []
		l = []
		n = []

		manzanas = self.datos.execute("SELECT manzana FROM PROPIETARIOS")
		lotes = self.datos.execute("SELECT lote FROM PROPIETARIOS")
		nomapes = self.datos.execute("SELECT nomape FROM PROPIETARIOS")
		manzanas = [i["manzana"] for i in manzanas]
		lotes = [i["lote"] for i in lotes]
		nomapes = [i["nomape"] for i in nomapes]

		for manzana in manzanas:
			if manzana not in m:
				m.append(manzana)

		for lote in lotes:
			if lote not in l:
				l.append(lote)

		for nomape in nomapes:
			if nomape not in n:
				n.append(nomape)

		self.cambiar_props(m, l, n)

	def cambiar_lotes(self, m, l):
   #     print("Adentro de cambiar lotes, recibimos", m, l)

		m.append("Manzana")
		l.append("Lote")

		self.l_menu_manz.destroy()
		self.l_menu_manz = CrearMenu(
			self.frame_lotes, self.l_var_m, m, comando=self.func_lotes, width=10)
		Gridear(self.l_menu_manz, 0, 0, py=5, px=10, sticky="ew")

		self.l_menu_lote.destroy()
		self.l_menu_lote = CrearMenu(
			self.frame_lotes, self.l_var_l, l, comando=self.func_lotes, width=10)
		Gridear(self.l_menu_lote, 0, 1, py=5, px=10, cs=2, sticky="ew")

	def cambiar_props(self, m, l, n):
		m.append("Manzana")
		l.append("Lote")
		n.append("Nombre")

		self.p_menu_manz.destroy()
		self.p_menu_manz = CrearMenu(
			self.frame_props, self.p_var_m, m, comando=self.func_props, width=6)
		Gridear(self.p_menu_manz, 0, 0, py=5, px=(10, 5), sticky="ew")

		self.p_menu_lote.destroy()
		self.p_menu_lote = CrearMenu(
			self.frame_props, self.p_var_l, l, comando=self.func_props, width=6)
		Gridear(self.p_menu_lote, 0, 1, py=5, px=(5, 5), sticky="ew")



		self.p_menu_nomb.destroy()
		self.p_menu_nomb = CrearMenu(
			self.frame_props, self.p_var_na, n, comando=self.func_props, width=6)
		Gridear(self.p_menu_nomb, 0, 2, py=5, px=(5, 10), sticky="ew")


class Consumos(Menu):
	def __init__(self, titulo, principal, datos):
		super().__init__(titulo)
		self.principal = principal
		self.datos = datos
		self.boton_atras = boton_atras(
			self.frame, lambda: self.volver(self.principal), ico=ArrowBackIcon)

		self.frame_consultas = CrearFrame(self.frame, bg="gray")
		self.frame_actualizar = CrearFrame(self.frame, bg="gray")
		self.frame_actualizar.rowconfigure(12, weight=1)

		self.var_m = StringVar()
		self.var_m.set("Manzana")
		self.var_l = StringVar()
		self.var_l.set("Lote")
		self.var_na = StringVar()
		self.var_na.set("Nombre")

		ms = []
		ls = []
		ns = []

		manzanas = self.datos.execute("SELECT man FROM CONSUMOS")
		lotes = self.datos.execute("SELECT lot FROM CONSUMOS")
		nombres = self.datos.execute("SELECT nombre  FROM CONSUMOS")

		manzanas = [i["man"] for i in manzanas]
		lotes = [i["lot"] for i in lotes]
		nombres = [i["nombre"] for i in nombres]


		for manzana in manzanas:
			if manzana not in ms:
				ms.append(manzana)

		for lote in lotes:
			if lote not in ls:
				ls.append(lote)

		for nombre in nombres:
			if nombre not in ns:
				ns.append(nombre)

		ms.sort()
		ms.append("Manzana")
		ls.sort()
		ls.append("Lote")
		ns.sort()
		ns.append("Nombre")

		self.menu_manz = CrearMenu(
			self.frame_consultas, variable=self.var_m, opciones=ms,  comando=self.cambiarTabla, width=6)
		self.menu_lote = CrearMenu(
			self.frame_consultas, variable=self.var_l, opciones=ls,  comando=self.cambiarTabla, width=6)
		self.menu_nomb = CrearMenu(
			self.frame_consultas, variable=self.var_na, opciones=ns,  comando=self.cambiarTabla, width=6)

		self.frame_muestra = CrearFrame(
			self.frame_consultas, bg=color["contraste"])
		self.scrollbar = Scrollbar(self.frame_consultas)
		self.listbox = CrearListbox(self.frame_muestra)
		self.listbox.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.listbox.yview)

		self.labels = [
			CrearLabel(self.frame_actualizar,
					   "Seguridad total:", 18, anchor="w"),
			CrearLabel(self.frame_actualizar, "Kw de luz:", 18, anchor="w"),
			CrearLabel(self.frame_actualizar, "M3 de agua:", 18, anchor="w"),
			CrearLabel(self.frame_actualizar, "M3 de gas:", 18, anchor="w"),
			CrearLabel(self.frame_actualizar, "Luz total:", 18, anchor="w"),
			CrearLabel(self.frame_actualizar,
					   "Agua por frente:", 18, anchor="w"),
			CrearLabel(self.frame_actualizar, "Asfalto:", 18, anchor="w"),
			CrearLabel(self.frame_actualizar, "Cocheras p/v:", 18, anchor="w"),
			CrearLabel(self.frame_actualizar,
					   "Valor m2 terreno:", 18, anchor="w"),
		]
		self.entries = [
			CrearEntry(self.frame_actualizar, width=8, altoLetra=18),
			CrearEntry(self.frame_actualizar, width=8, altoLetra=18),
			CrearEntry(self.frame_actualizar, width=8, altoLetra=18),
			CrearEntry(self.frame_actualizar, width=8, altoLetra=18),
			CrearEntry(self.frame_actualizar, width=8, altoLetra=18),
			CrearEntry(self.frame_actualizar, width=8, altoLetra=18),
			CrearEntry(self.frame_actualizar, width=8, altoLetra=18),
			CrearEntry(self.frame_actualizar, width=8, altoLetra=18),
			CrearEntry(self.frame_actualizar, width=8, altoLetra=18),

		]

		self.cambiarTabla(None)

		self.cambiar_precios = CrearButton(
			self.frame_consultas, text="Cambiar precios", width=30, height=1, command=self.mostrar_actualizar_datos)
		self.guardar = CrearButton(self.frame_actualizar, text="Guardar cambios",
								   width=30, height=1, command=self.guardar_cambios)
		self.volver_c = CrearButton(self.frame_actualizar, text="Volver a consumos",
									width=30, height=1, command=self.mostrar_consumos)

	def guardar_cambios(self):
		l = []
		for i in self.entries:
			l.append(i.get())
		l2 = []

		try:
			for i in l:
				l2.append(int(i))
		except:
			messagebox.showerror("Error", "Ingrese números")

		else:
			self.datos.execute("DELETE FROM Costos")
			self.datos.execute("INSERT INTO Costos Values(?,?,?,?,?,?,?,?,?)", *l2)

			self.datos.actualizar()
			self.cambiarTabla(None)

		# print(self.datos.costos)

	def mostrar(self):
		self.cambiar_menues()

		try:
			self.principal.esconder()
		except:
			pass  # TODO: hace falta?

		Gridear(self.frame, 1, 0, cs=2)

		if not self.f:

			self.f = True
			Gridear(self.titulo, 1, 0, cs=2, py=(20, 20))

			self.mostrar_consumos()

			Gridear(self.cambiar_precios, 10, 0, cs=3, px=20, py=15, sticky="")

			Gridear(self.guardar, 11, 0, cs=2,  px=46, py=15)
			Gridear(self.volver_c, 12, 0, cs=2,  px=46, py=15)

			Gridear(self.boton_atras, 13, 0, cs=2, sticky="sw", py=20, px=20)

	def mostrar_actualizar_datos(self):
		self.frame_consultas.grid_forget()
		Gridear(self.frame_actualizar, 3, 0, cs=2)

		datos_costos = self.datos.execute("SELECT * FROM Costos")

		for i in range(len(self.labels)):
			Gridear(self.labels[i], i, 0, px=7)
			Gridear(self.entries[i], i, 1, px=7)
			self.entries[i].delete(0, END)
			self.entries[i].insert(0, datos_costos[0][i])


	def mostrar_consumos(self):
		self.frame_actualizar.grid_forget()
		Gridear(self.frame_consultas, 3, 0, cs=3)
		Gridear(self.menu_manz, 0, 0, py=5, px=(10, 5), sticky="ew")
		Gridear(self.menu_lote, 0, 1, py=5, px=(5, 5), sticky="ew")
		Gridear(self.menu_nomb, 0, 2, py=5, px=(5, 10), sticky="ew")
		Gridear(self.frame_muestra, 1, 0, cs=3, px=5)
		Gridear(self.scrollbar, 1, 2, cs=1, sticky="nse", px=5)
		Gridear(self.listbox, 1, 0, cs=2)

	def cambiarTabla(self, _dato):
		self.listbox.delete(0, END)

		m = self.var_m.get()
		try:
			m = int(m)
		except:
			pass

		l = self.var_l.get()
		try:
			l = int(l)
		except:
			pass

		n = self.var_na.get()

		lineas = 0

		datos = self.datos.execute("SELECT * FROM CONSUMOS")

		for i in range(len(datos)):

			if m != "Manzana":
				if m != datos[i]["man"]:
					continue

			if l != "Lote":
				if l != datos[i]["lot"]:
					continue

			if n != "Nombre":
				if n != datos[i]["nombre"]:
					continue

			string = ["Recibo de {}".format(datos[i]["nombre"]),
					  "Lote: {}, manzana: {}".format(
						  datos[i]["lot"], datos[i]["man"]),
					  "Valor del lote -- ${:,.2f}".format(
				datos[i]["terreno"]),
				"Seguridad  ---------  ${:,.2f}".format(
				datos[i]["seguridad"]),
				"Electricidad  ------  ${:,.2f}".format(
				datos[i]["luz"]),
				"Agua  --------------  ${:,.2f}".format(
				datos[i]["agua"]),
				"Gas  ---------------  ${:,.2f}".format(
				datos[i]["gas"]),
				"Luz pública  -------  ${:,.2f}".format(
				datos[i]["luz_publica"]),
				"Metros de frente  --  ${:,.2f}".format(
				datos[i]["f_agua"]),
				"Metros asfaltados  -  ${:,.2f}".format(
				datos[i]["f_asf"]),
				"Cocheras  ----------  ${:,.2f}".format(
				datos[i]["vehiculo"]),
				"",
				"#"*33,
				"",
				"Total  -------------  ${:,.2f}".format(datos[i]["seguridad"]+datos[i]["luz"]+datos[i]["agua"]+datos[i]["gas"]
														+datos[i]["luz_publica"]+datos[i]["f_agua"]+datos[i]["f_asf"]+datos[i]["vehiculo"]),
				"",
				"#"*33,
				"",
			]

			for i in range(len(string)):
				self.listbox.insert(i, string[i])

	def cambiar_menues(self):
		m = []
		l = []
		n = []

		manzanas = self.datos.execute("SELECT man FROM CONSUMOS")
		lotes = self.datos.execute("SELECT lot FROM CONSUMOS")
		nombres = self.datos.execute("SELECT nombre FROM CONSUMOS")


		manzanas = [i["man"] for i in manzanas]
		lotes = [i["lot"] for i in lotes]
		nombres = [i["nombre"] for i in nombres]

		for manzana in manzanas:
			if manzana not in m:
				m.append(manzana)

		for lote in lotes:
			if lote not in l:
				l.append(lote)

		for nombre in nombres:
			if nombre not in n:
				n.append(nombre)



		m.append("Manzana")
		l.append("Lote")
		n.append("Nombre")

		self.menu_manz.destroy()
		self.menu_manz = CrearMenu(
			self.frame_consultas, self.var_m, m, comando=self.cambiarTabla, width=6)
		Gridear(self.menu_manz, 0, 0, py=5, px=(10, 5), sticky="ew")

		self.menu_lote.destroy()
		self.menu_lote = CrearMenu(
			self.frame_consultas, self.var_l, l, comando=self.cambiarTabla, width=6)
		Gridear(self.menu_lote, 0, 1, py=5, px=(5, 5), sticky="ew")

		self.menu_nomb.destroy()
		self.menu_nomb = CrearMenu(
			self.frame_consultas, self.var_na, n, comando=self.cambiarTabla, width=6)
		Gridear(self.menu_nomb, 0, 2, py=5, px=(5, 10), sticky="ew")

	def actualizar_datos(self):
	  #  print("Se cambiaron los precios")
		self.datos.actualizar()


# ----------------------------------------------------- Configuración inicial ----
h = 768 - 768 / 12
raiz = Tk()
raiz.config(bg=color["fondo"], width=h / 1.4, height=h)

raiz.grid_propagate(0)
raiz.grid_columnconfigure(0, weight=1)
raiz.grid_rowconfigure(1, weight=1)

raiz.title("Administración de barrios privados")
raiz.resizable(0, 0)  # TODO:


# ----------------------------------------------------- iconos,  ----
try:
	AddHomeWorkIcon = PhotoImage(file=r"Iconos\AddHomeWork.png")
	GroupAddIcon = PhotoImage(file=r"Iconos\GroupAdd.png")
	ManageSearchIcon = PhotoImage(file=r"Iconos\ManageSearch.png")
	PaymentsIcon = PhotoImage(file=r"Iconos\Payments.png")
	ArrowBackIcon = PhotoImage(file=r"Iconos\ArrowBack.png")
	SaveIcon = PhotoImage(file=r"Iconos\Save.png")
except:
	AddHomeWorkIcon = ""
	GroupAddIcon = ""
	ManageSearchIcon = ""
	PaymentsIcon = ""
	ArrowBackIcon = ""
	SaveIcon = ""
	print("No se encontraron los iconos!!")


##
header = CrearLabel(raiz, "Administración de\nBarrios Privados",
					24, bg=color["contraste"], fg=color["acento"])
Gridear(header, 0, 0, ipy=0, cs=2)

##
principal = Principal(["Alta de\nlotes", "Alta de\npropietarios", "Consultas", "Consumos"],
					  [AddHomeWorkIcon, GroupAddIcon, ManageSearchIcon,
						  PaymentsIcon, ArrowBackIcon],
					  )

clase_datos = Datos("DB.db")

clase_datos.actualizar()

lotes = Lotes("Alta de lotes", principal, clase_datos)
propietarios = Propietarios("Alta de propietarios", principal, clase_datos)
consultas = Consultas("Consultas", principal, clase_datos)
consumos = Consumos("Consumos", principal, clase_datos)


principal.setearComandos([lambda: principal.a(lotes), lambda: principal.a(
	propietarios), lambda: principal.a(consultas), lambda: principal.a(consumos)])


principal.mostrar()

raiz.mainloop()
