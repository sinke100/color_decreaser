import PIL.Image as im
from math import sqrt
import numpy as np 
from io import BytesIO as by
import PySimpleGUI as sg
sg.theme('Python')
koraci = [str(i) for i in range(1,201)]
ikona = np.ones((30,30,3),np.uint8)*255
ikona[0:15,0:15] = 255,0,0
ikona[0:15,15:30] = 0,255,0
ikona[15:30,0:15] = 0,0,255
ikona = im.fromarray(ikona)
def provjera(t, x, y):
	if len(x) == 3:
		a, b, c = abs(x[0]-y[0]), abs(x[1]-y[1]), abs(x[2]-y[2])
		return sqrt(a**2+b**2+c**2) < t
	else:
		a, b, c, d = abs(x[0]-y[0]), abs(x[1]-y[1]), abs(x[2]-y[2]), abs(x[3]-y[3])
		return sqrt(a**2+b**2+c**2+d**2) < t
def nova_farba(t, x, sve_f):
        if len(x) == 3:
                for _,y in sve_f:
                        a, b, c = abs(x[0]-y[0]), abs(x[1]-y[1]), abs(x[2]-y[2])
                        if sqrt(a**2+b**2+c**2) < t: return y
        else:
                for _,y in sve_f:
                        a, b, c, d = abs(x[0]-y[0]), abs(x[1]-y[1]), abs(x[2]-y[2]), abs(x[3]-y[3])
                        if sqrt(a**2+b**2+c**2+d**2) < t: return y
def kreiraj(s):
	w, h = s.size
	if w > 800: s = s.resize((w//2,h//2))
	output = by()
	s.save(output, 'PNG')
	s = output.getvalue()
	return s
def glavna(t, img_org):
    w,h = img_org.size
    kanali = 4 if img_org.mode == 'RGBA' else 3 
    img_list = list(img_org.getdata())
    k = list(dict.fromkeys(img_list))
    k = {i:0 for i in k}
    for i in img_list: k[i]+=1
    sve = sorted([[i, j] for j, i in k.items()], reverse=True)
    farbe = [i[1] for i in sve]
    #print('Ukupno boja',len(farbe))
    farbe_f = []
    for i in farbe:
        for j in farbe_f:
            if provjera(t, i, j): break
        else: farbe_f.append(i)
    sve_f = [i for i in sve if i[1] in farbe_f]
    img_nova = [nova_farba(t, i, sve_f) for i in img_list]
    img_nova = [i if i else (255,)*kanali for i in img_nova]
    
    #print('Ukupno smanjenih boja',len(sve_f))
    #if len(sve_f)<=10: print([i[1] for i in sve_f])
    img_nova = np.array(img_nova, np.uint8).reshape((h,w,kanali))
    img_nova = im.fromarray(img_nova)
    return img_nova, len(farbe), len(sve_f)
def ly(x, s_org=b'',s_novi=b'',bf_org=0,bf_novi=0):
        cl1 = sg.Column([[sg.Text('Upiši file')],[sg.Text('Upiši broj koraka (1-200) [manji korak znaci vise otkrivenih boja]')]],element_justification='left')
        cl2 = sg.Column([[sg.Input(size=30)],[sg.Input(size=30)]],element_justification='right')
        #layout1 = [[sg.Text('Upiši file'), sg.Input(size=30)],[sg.Text('Upiši broj koraka (1-200) [manji korak znaci vise otkrivenih boja]'), sg.Input(size=30)],[sg.Button('Dalje')]]
        layout1 = [[cl1,cl2],[sg.Button('Dalje')]]
        layout2 = [[sg.Image(s_org),sg.Image(s_novi)],[sg.Text(f'Broj boja u originalu {bf_org}')],[sg.Text(f'Broj boja u novoj slici {bf_novi}')],[sg.Button('Ponovo'), sg.Button('Save')],[sg.Text('Spremljeno',visible=False,k='dp')]]
        return vars()[f'layout{x}']
def window(info=False):
    if info:
        slika_org, slika_nova, naziv, korak, farbe_org, farbe_nove = info
        slika_org = kreiraj(slika_org)
        slika_nova = kreiraj(slika_nova)
        win = sg.Window('',ly(2,slika_org,slika_nova,farbe_org,farbe_nove),font=('Verdana',20))
        win.WindowIcon = kreiraj(ikona)
    else:
            win = sg.Window('',ly(1),font=('Verdana',20))
            win.WindowIcon = kreiraj(ikona)
    while True:
        e,v = win.read()
        dalje = True
        if e == None: return [e]*2
        if e == 'Dalje':
            file = v[0]
            try:
                img_org = im.open(file)
            except FileNotFoundError:
                win[0].update('')
                dalje = False
            korak = v[1]
            if korak not in koraci:
                win[1].update('')
                dalje=False
            if not dalje: continue
            naziv = file.split('.')[0]
            korak = int(korak)
            win.close()
            img_nova, fo, fn = glavna(korak, img_org)
            info = img_org, img_nova, naziv, korak, fo, fn
            return e, info
        if e == 'Save':
            with open(f'{naziv}_{korak}_{farbe_nove}.png','wb') as f: f.write(slika_nova)
            win['dp'].update(visible=True)
        
        else:
            win.close()
            return [e]*2
prozor = 'Ponovo'
while prozor:
    if prozor == 'Ponovo': prozor,info = window()
    else: prozor,info = window(info)
