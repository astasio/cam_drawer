#!/usr/bin/env python

import gio
import atk
import gtk
import cairo
import pango
import pangocairo
import os

memory='cam_drawer.txt'
width=840
height=440
prog=[]

try:
	buff=file(memory,"r")
	buff.close()
except:
	buff=file(memory,"w")
	buff.close()

def refresh():
	buff=file(memory,'r')
	tb=gtk.TextBuffer()
	testo=''
	for i in buff.readlines():
		testo=testo+str(i)
	tb.set_text(testo)
	textview.set_buffer(tb)
	buff.close()
	
def command():	
	tb=textview.get_buffer()
	start=tb.get_start_iter()
	end=tb.get_end_iter()
	testo=tb.get_text(start,end)
	buff=file(memory,'w')
	buff.write(testo)
	buff.close()
	screen.hide()
	screen.show()
	expose(screen,'expose_event')

def expose(widget,event):
	del prog[0:-1]
	traduce()
	cr=widget.window.cairo_create()
	for i in prog:
                exec(i)
        exec("cr.stroke()")	
	

def traduce():
	buff=file(memory,'r')
	v=0
	o=0
	r=0
	for i in buff.readlines():
		try:
			if(i.upper().split()[0]=="G0"):
				status.push(0,"G0")
				if(i.split()[1][0].upper()=="X"):
					v=i.upper().split()[1].split("X")[1]
				elif(i.split()[1][0].upper()=="Z"):
					o=i.upper().split()[1].split("Z")[1]
	
	
				try:
					if(i.split()[2][0].upper()=="X"):
						v=i.upper().split()[2].split("X")[1]
	
					elif(i.split()[2][0].upper()=="Z"):
						o=i.upper().split()[2].split("Z")[1]
				except:
					pass	
				prog.append("cr.move_to("+str(o)+","+str(v)+")")
			

			if(i.split()[0].upper()=="G1"):
				status.push(0,"G1")
				if(i.split()[1][0].upper()=="X"):
					v=i.upper().split()[1].split("X")[1]
				elif(i.split()[1][0].upper()=="Z"):
					o=i.upper().split()[1].split("Z")[1]
				try:
					if(i.split()[2][0].upper()=="X"):
						v=i.upper().split()[2].split("X")[1]
					elif(i.split()[2][0].upper()=="Z"):
						o=i.upper().split()[2].split("Z")[1]	
				except:
					pass
				prog.append("cr.line_to("+str(o)+","+str(v)+")")
				
	
			elif(i.split()[0].upper()=="G2"):
				status.push(0,"G2")
				vp=v
				op=o
				if(i.split()[1][0].upper()=="X"):
					v=i.upper().split()[1].split("X")[1]
				elif(i.split()[1][0].upper()=="Z"):
					o=i.upper().split()[1].split("Z")[1]
				if(i.split()[2][0].upper()=="X"):
					v=i.upper().split()[2].split("X")[1]
				elif(i.split()[2][0].upper()=="Z"):
					o=i.upper().split()[2].split("Z")[1]
				r=i.upper().split()[3].split("CR=")[1]
		
				vm=0
				om=0			
				if(int(op)<int(o) and int(vp)>int(v)):
					vm=v
					om=op
				elif(int(op)<int(o) and int(vp)<int(v)):
					vm=vp
					om=o
				elif(int(vp)<int(v) and int(op)>int(o)):
					vm=v
					om=op
				elif(int(op)>int(o) and int(vp)>int(v)):
					vm=vp
					om=o	
				prog.append("cr.curve_to("+str(op)+","+str(vp)+","+str(om)+","+str(vm)+","+str(o)+","+str(v)+")")
	
			elif(i.split()[0].upper()=="G3"):
				status.push(0,"G3")
				vp=v
				op=o
				if(i.split()[1][0].upper()=="X"):
					v=i.upper().split()[1].split("X")[1]
				elif(i.split()[1][0].upper()=="Z"):
					o=i.upper().split()[1].split("Z")[1]
				if(i.split()[2][0].upper()=="X"):
					v=i.upper().split()[2].split("X")[1]
				elif(i.split()[2][0].upper()=="Z"):
					o=i.upper().split()[2].split("Z")[1]
				r=i.upper().split()[3].split("CR=")[1]
	
				vm=0
				om=0
			
				if(int(op)>int(o) and int(vp)>int(v)):
					vm=v
					om=op    
				elif(int(op)>int(o) and int(vp)<int(v)):
					vm=vp
					om=o
				elif(int(vp)<int(v) and int(op)<int(o)):
					vm=v
					om=op
				elif(int(op)<int(o) and int(vp)>int(v)):
					vm=vp
					om=o
				prog.append("cr.curve_to("+str(op)+","+str(vp)+","+str(om)+","+str(vm)+","+str(o)+","+str(v)+")")	
			else:
				if(i.upper().split()[0][0]=="X"):
					v=i.upper().split()[0].split("X")[1]
					try:
						o=i.upper().split()[1].split("Z")[1]
					except:
						pass
				elif(i.upper().split()[0][0]=="Z"):
					o=i.upper().split()[0].split("Z")[1]
					try:
						v=i.upper().split()[1].split("X")[1]
					except:
						pass
	
				if(status.get_children().__getitem__(0).get_child().get_children()[0].get_text()=="G0"	):			
					prog.append("cr.move_to("+str(o)+","+str(v)+")")
					
				elif(status.get_children().__getitem__(0).get_child().get_children()[0].get_text()=="G1"):
					prog.append("cr.rel_line_to("+str(o)+","+str(v)+")")
			buff.close()
		except:
			pass
			


def stampa():
	pdfs=cairo.PDFSurface("cam_drawer.pdf",800,400)
	cr=cairo.Context(pdfs)
	for i in prog:
		exec(i)
	exec("cr.stroke()")
	buff.close()
	pdfs.finish()
	os.system("evince cam_drawer.pdf")

def exit():
	gtk.main_quit()

win= gtk.Window()
win.connect("destroy",lambda *w:exit())
win.set_title("Cam_Drawer")
win.set_resizable(False)
vbox=gtk.VBox()
win.add(vbox)
vbox.set_homogeneous(False)

screen=gtk.DrawingArea()
screen.set_events(gtk.gdk.BUTTON_PRESS_MASK)
screen.set_size_request(width,height)
vbox.add(screen)	
vbox.set_child_packing(screen,expand=False,fill=False, padding=0,pack_type=gtk.PACK_START)
screen.connect('expose_event',expose)
#screen.connect("button_press_event",lambda *w: click())
screen.modify_bg(gtk.STATE_NORMAL,gtk.gdk.color_parse("#aaa"))

scroll=gtk.ScrolledWindow()
scroll.set_size_request(800,200)
vbox.add(scroll)
textview=gtk.TextView()
scroll.add(textview)

h=gtk.HBox()
vbox.add(h)
h.set_homogeneous(False)

put=gtk.Button('Invio')
h.add(put)
h.set_child_packing(put,expand=True,fill=True, padding=10,pack_type=gtk.PACK_START)
put.connect('clicked',lambda *w: command())

put2=gtk.Button('Stampa')
h.add(put2)
h.set_child_packing(put2,expand=False,fill=False, padding=10,pack_type=gtk.PACK_END)
put2.connect('clicked',lambda *w: stampa())

status=gtk.Statusbar()
vbox.add(status)
vbox.set_child_packing(status,expand=False,fill=False, padding=0,pack_type=gtk.PACK_END)
refresh()

win.show_all()

gtk.main()
