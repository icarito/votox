# *-* coding: utf-8 *-*
import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.rst import RstDocument
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput

import csv
import random

import hashlib
import requests
#import json

#### INTRO
intro_text = """
==================
VOTOX - Bienvenido
==================
**Sistema distribuído de reporte y conteo de votos.**

Utilizando este sistema podrás reportar tu voto, el cual será contabilizado dentro de la cadena global de bloques *"blockchain"* de metadatos, la cual no puede ser tergiversada ni adulterada por entidad alguna.

El objetivo de VOTOX es ofrecer un sistema *paralelo, ciudadano, descentralizado* de registro público de la emisión de un voto. Herramientas como esta podrían jugar un rol importante en la **modernización de los sistemas de votación** al ofrecer una **infraestructura paralela** capaz de registrar en forma segura las **opciones de los ciudadanos**.
"""

#### RESULT
result_text = """
=================
VOTOX - Resultado
=================
**Sistema distribuído de reporte y conteo de votos.**

El sistema reportará ahora su opción a la cadena de bloques *"blockchain"*. Por favor espere su confirmación a continuación.
"""

#### PARA EL VOTO
candidatos = []
with open('Candidatos _Presidenciales-2006-2011-2016.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[1]=='2016':
            candidatos.append(row)

class MyApp(App):

    def build(self):

        sm = ScreenManager()
        sm.add_widget(Screen(name='intro'))
        sm.add_widget(Screen(name='vote'))
        sm.add_widget(Screen(name='result'))

        #### INTRO
        def goto_vote(instance):
            if len(self.dniinput.text)==8:
                self.popup.dismiss()
                self.dni = self.dniinput.text
                self.sm.current = 'vote'

        def goto_dni(instance):
            layout = BoxLayout(padding=10,
                                orientation='vertical')
            dniinput = TextInput(text='',
                                multiline=False,
                                size_hint=(1, 0.2))
            confirm_btn = Button(text='CONTINUAR',
                                size_hint=(1, 0.2))
            layout.add_widget(dniinput)
            layout.add_widget(confirm_btn)
            popup = Popup(title=u'Porfavor ingresa tu DNI',
                                content=layout,
                                size_hint=(None, None), size=(400, 400))
            confirm_btn.bind(on_press=goto_vote)
            self.popup=popup
            self.dniinput=dniinput
            popup.open()

        intro = sm.get_screen('intro')
        welcome = RstDocument(text=intro_text)
        layout = AnchorLayout(padding=10,
                            orientation='vertical')
        layout.add_widget(welcome)
        layout.add_widget(Button(text='Reportar Mi Voto', 
                                size_hint=(0.1, 0.1),
                                on_press=goto_dni))
        intro.add_widget(layout)

        #### VOTO
        def goto_result(instance):
            self.sm.current = 'result'
            self.popup.dismiss()
            self.send_vote()

        def goto_confirm(instance):
            layout = BoxLayout(padding=10,
                                orientation='vertical')
            layout.add_widget(Label(text=instance.text))
            btn_layout = BoxLayout(padding=10,
                                orientation='horizontal',
                                size_hint=(1, 0.2),
                                )
            confirm_btn = Button(text='CONFIRMAR')
            cancel_btn = Button(text='CANCELAR')
            btn_layout.add_widget(confirm_btn)
            btn_layout.add_widget(cancel_btn)
            layout.add_widget(btn_layout)
            popup = Popup(title=u'Confirma tu Opción',
                                content=layout,
                                size_hint=(None, None), size=(400, 400))
            cancel_btn.bind(on_press=popup.dismiss)
            confirm_btn.bind(on_press=goto_result)
            self.popup=popup
            self.opcion = instance.text
            popup.open()

        voto = sm.get_screen('vote')
        layout = BoxLayout(padding=10,
                            orientation='vertical')

        random.shuffle(candidatos)
        for cand in candidatos:
            layout.add_widget(Button(text=cand[4],
                                on_press=goto_confirm))
        voto.add_widget(layout)

        ### RESULT

        result = sm.get_screen('result')
        goodbye = RstDocument(text=result_text)
        layout = AnchorLayout(padding=10,
                            orientation='vertical')
        layout.add_widget(goodbye)
        layout.add_widget(ProgressBar(value=20))
        result.add_widget(layout)

        self.sm = sm
        return sm

    def send_vote(self):
        uniq = hashlib.sha1(self.dni).hexdigest()
        vote = {'uniq':uniq, 'opcion':self.opcion}

        try:
            r = requests.post('http://pad.somosazucar.org:5000/vote', data=vote)
        except:
            print "SERVIDOR NO ENCONTRADO"

if __name__ == '__main__':
    MyApp().run()
