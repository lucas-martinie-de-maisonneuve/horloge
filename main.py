import time
import threading
import keyboard
import sys

choix_mode_affichage = input("""
                Une fois l'horloge configurée, appuyez sur 'p' 
                pour la mettre en pause et accéder aux options
                
                Voulez-vous utiliser le mode d'affichage 12 heures ? (O/N):
                """).upper()

pause_horloge = False
stop_threads = False

h_alarme, m_alarme, s_alarme = 0, 0, 0
h, m, s = 0, 0, 0

def horloge():
    global pause_horloge
    global h
    global m
    global s
    while True:
        if not pause_horloge:
            if s < 59:
                time.sleep(1)
                s += 1
            elif m < 59:
                m += 1
                s = 0
            else:
                h += 1
                m = 0
                s = 0
                
            sys.stdout.write("\r")  # Retour à la ligne précédente
            sys.stdout.flush()

            if choix_mode_affichage == 'O':
                mode_affichage(h, m, s)
            else:
                print(f"Heure actuelle : {str(h).zfill(2)}:{str(m).zfill(2)}:{str(s).zfill(2)}")
            
            verifier_alarme()

        if stop_threads:
            break

def config_alarme():
    global h_alarme
    global m_alarme
    global s_alarme
    set_alarm = tuple(input("""
                Configurer l'alarme (format hh mm ss): 
                """).split())
    h_alarme = int(set_alarm[0])
    m_alarme = int(set_alarm[1])
    s_alarme = int(set_alarm[2])

def verifier_alarme():
    if h == h_alarme and m == m_alarme and s == s_alarme:
        print("C'est l'heure de l'alarme")

def mode_affichage(h, m, s):
    if h >= 12:
        am_pm = "PM"
        if h > 12:
            h -= 12
    else:
        am_pm = "AM"
    print(f"Heure actuelle : {str(h).zfill(2)}:{str(m).zfill(2)}:{str(s).zfill(2)} {am_pm}")

def afficher_heure():
    global h
    global m
    global s
    reglage = tuple(input("""
                Reglage de l'heure (format hh mm ss): 
                """).split())
    h = int(reglage[0])
    m = int(reglage[1])
    s = int(reglage[2])

    return h, m, s

def toggle_pause():
    global pause_horloge
    pause_horloge = not pause_horloge
    if pause_horloge:
        print("""
                -----------------------------------------
                Appuyez sur 'p' pour redémarrer l'horloge.
                Appuyez sur 's' pour éteindre l'horloge
                Appuyez sur 'a' pour configurer l'alarme
                Appuyez sur 'r' pour configurer l'heure
                -----------------------------------------
                """)
    else:
        print("Horloge reprise.")
heure = afficher_heure()

horloge_thread = threading.Thread(target=horloge)

horloge_thread.start()

while True:
    if keyboard.is_pressed('p'):
        toggle_pause()
        time.sleep(0.2)
    elif keyboard.is_pressed('s'):
        print("Arrêt du script.")
        stop_threads = True
        break
    elif keyboard.is_pressed('a'):
        config_alarme()
        time.sleep(0.2)
    elif keyboard.is_pressed('r'):
        afficher_heure()
        time.sleep(0.2)
