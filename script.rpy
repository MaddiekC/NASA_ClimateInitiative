#script .rpy
init python:
    import csv
    import os

    # Cargar el dataset desde un archivo CSV
    archivo_csv = os.path.join(config.basedir, "game",  "pilot_topdown_CO2_Budget_countries_v1.csv")
    # Leer el archivo CSV y almacenar los datos en una lista
    dataset = []
    with open(archivo_csv, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Year'].isdigit():
                dataset.append(row)

    # Método para obtener información del país seleccionado
    def obtener_informacion(pais, anio):
        resultado = [row for row in dataset if row['Alpha 3 Code'] == pais and row['Year'] == str(anio)]
        if resultado:
            # Convertir el valor a un número flotante y formatearlo sin notación científica
            emisiones = float(resultado[0].get('FF (TgCO2)', '0'))
            return f"{emisiones:,.2f}"  # Formato con dos decimales y sin notación científica
        return None

    # Método para obtener información del país seleccionado 2
    def obtener_informacion2(pais2, anio):
        resultado = [row for row in dataset if row['Alpha 3 Code'] == pais and row['Year'] == str(anio)]
        if resultado:
            # Convertir el valor a un número flotante y formatearlo sin notación científica
            emisiones = float(resultado[0].get('FF (TgCO2)', '0'))
            return f"{emisiones:,.2f}"  # Formato con dos decimales y sin notación científica
        return None


# Coloca el código de tu juego en este archivo.

# Declara los personajes usados en el juego como en el ejemplo:

define e = Character("Eileen")
define protagonist = Character("Protagonist", color="#c8ffc8")
default co2_level=0
default show_computer = False  # Variable para mostrar el computador
#default emission_results = {}

# Pantalla personalizada del mapa
default mapa_clicked = False 

label second:
    # Pantalla personalizada del mapa
    screen Mapa_mundi:
        frame:
            xalign 0.5 ypos 50
            imagebutton:
                idle "art nocolormap.png"
                hover "art colormap.png"  
                action [SetVariable("mapa_clicked", True), Notify("Has hecho clic en el mapa de emisiones globales de CO2."), Jump("map_clicked")]  # Elimina el segundo Jump
                focus_mask True  # Hace que el botón reaccione al área no transparente de la imagen


# El juego comienza aquí.
label start:
    #Musica de ambiente
    scene bg room
    play sound "alarm-clock-short.mp3" fadeout 1
    "You wake up and open your eyes"
    play sound "morning-birdsong.mp3" fadeout 1
    "The morning light enters through your bedroom window, illuminating the books and posters that decorate the walls."
    # Mostrar la pantalla del mapa
    show screen Mapa_mundi

    "A world map with carbon emissions indicators catches your attention."
    while not mapa_clicked:
        "You may click the world map to continue"     
        pause

label map_clicked:
    hide screen Mapa_mundi
   
    protagonist "Wow... this global map is very interesting."
    protagonist "Those red spots in the United States and China... are like wounds on the planet."
    protagonist "And Europe is not far behind with all that orange."
    protagonist "I wonder how much of that is due to industry, how much is due to our lifestyle.."
    protagonist "It's easy to feel small and powerless in the face of such a big problem.."
    protagonist "But I guess every action counts, right? Even mine."
    protagonist "Maybe I should think about how I can reduce my own carbon footprint."
    protagonist "Or maybe I could learn more about it. Knowledge is power, after all.."
    protagonist "Although sometimes... sometimes I just want to ignore it all and get on with my life."
    
    "With these thoughts going around in your head, you step away from the map and get ready to start your day."
    jump actotwo


label actotwo:
    
    play music "music.ogg"
    scene bg desk
    with pixellate
    "After getting up you look at your room. The desk is in front of you."
    jump actothree

label actothree:
    "You stop to think and decide what to do."
    menu:
        "Go to the desk and research climate change.":
            jump choise_investigar
        "Waste time.":
            jump choise_entretenerse
        

label choise_entretenerse:
    menu:
        "You spend time on social media.":
            #$ tiempo_malgastado = true
            jump tiempo_malgastado
        "Think better about the decision.":
            jump actothree
            

label choise_investigar:
    # Configuración del país y fechas
    "Which country do you want to explore?"
    menu:
        "EEUU":
            $ pais = "USA"
        "Brasil":
            $ pais = "BRA"
        "India":
            $ pais = "IND"
    
    "You selected [pais]. What date would you like to explore??"
    menu:
        "2015":
            $ anio = 2015
        "2018":
            $ anio = 2018
        "2020":
            $ anio = 2020
    
    "You have chosen the date: [anio]."

    jump desk_view

# Funciones para mostrar gráficos
label show_co2_graph:
    
    python:
        # Llamamos a la función obtener_informacion para obtener las emisiones de CO2
        informacion = obtener_informacion(pais, anio)

        # Verificamos si hay datos disponibles
        if informacion is None:
            resultado_texto = f"No data found for the country {pais} in the year {anio}."
        else:
            resultado_texto = f"CO₂ emissions in {pais} in the year {anio} were {informacion} TgCO2."

    # Mostrar el resultado en el diálogo de Ren'Py
    "[resultado_texto]"
    jump comment_scene


label desk_view:
    # Escena del escritorio
    scene bg desk
    "On the desk there is a newspaper and a computer."
    
    # Condicional para mostrar el periódico y la computadora
    if not show_computer:
        "Do you want to read the newspaper or use the computer?"
    else:
        "Do you want to use the computer or look out the window?"

    menu:
        "Read the newspaper":
            jump newspaper_scene
        "Use the computer":
            $ show_computer = True
            jump computer_scene
        "Look out the window":
            jump window_scene

label newspaper_scene:
    # Escena del periódico
    scene bg newspaper
    "Here is the newspaper with data on climate change."
    
    # Información sobre CO2 (esto se puede modificar con datos reales)
    $ co2_level = renpy.random.randint(350, 450)  # Simular niveles de CO2
    
    "The newspaper reports that the level of CO₂ in [pais] is [co2_level] ppm."
    
    "Do you want to know more about the impact of climate change in [pais]?"
    
    menu:
        "Yes":
            scene bg graficoperi
            "Interesting! The increase in CO₂ levels has led to drastic changes in the climate."
            jump window_scene
        "No":
            "You decide not to read any more and look out the window."
            jump window_scene

label window_scene:
    # Escena de la ventana
    #scene bg window
    "You look out the window and observe the surroundings."
    
    # Comentario del personaje según el nivel de CO2
    if co2_level > 400:
        scene bg cont
        "You see the sky covered in smog. Climate change is evident here."
    else:
        scene bg cielo
        "The climate seems normal, but we know that CO₂ is still a problem."
        
    # Botón para avanzar el tiempo
    "Do you want to move forward in time?"
    menu:
        "Yes":
            jump time_advance
        "No":
            "You decide to stay a little longer watching."

label time_advance:
    # Escena del cambio de tiempo
    scene bg night
    # show eileen sad 
    "The atmosphere has changed."
    scene bg computer
    "Now let's see from the computer."
    $ show_computer = True  # Mostrar computadora

    jump computer_scene  # Llevar al jugador a la escena de la computadora

label computer_scene:
    # Escena del computador en el escritorio
    scene bg computer
    "On the computer, you can explore data about climate change."
    
    # Interacción con la computadora
    "What would you like to see?"
    menu:
        "CO₂ levels":
            "Displaying graphs of CO₂ levels.."
            jump show_co2_graph
            #jump comment_scene
        "Compare with another country":
            "Select another country to compare."
            jump compare_country

label compare_country:
    "Which country do you want to compare with [pais]?"
    menu:
        "China":
            $ pais2 = "CHN"
        "Australia":
            $ pais2 = "AUS"
        "Ecuador":
            $ pais2 = "ECU"

    "You have chosen to compare with [pais2]."

    python:
        # Llamamos a la función obtener_informacion para obtener las emisiones de CO2
        informacion = obtener_informacion2(pais2, anio)

        # Verificamos si hay datos disponibles
        if informacion is None:
            resultado_texto = f"No data found for {pais2} in the year {anio}."
        else:
            resultado_texto = f"CO₂ emissions in {pais2} in the year {anio} were {informacion} TgCO2."

    # Mostrar el resultado en el diálogo de Ren'Py
    "[resultado_texto]"

    jump graficos  


label graficos:
    if pais == 'BRA' and pais2 == 'CHN':
        scene bg brazil_chn
        "MShowing the chart for Brasil and China."
    elif pais == 'BRA' and pais2 == 'AUS':
        scene bg brazil_aus
        "Showing the chart for Brasil and Australia."
    elif pais == 'BRA' and pais2 == 'ECU':
        scene bg brazil_ecu
        "Showing the chart for Brasil and Ecuador."
    elif pais == 'USA' and pais2 == 'CHN':
        scene bg usa_chn
        "Showing the chart for United States and China."
    elif pais == 'USA' and pais2 == 'AUS':
        scene bg usa_aus 
        "Showing the chart for United States and Australia."
    elif pais == 'USA' and pais2 == 'ECU':
        scene bg usa_ecu  
        "Showing the chart for United States and Ecuador."
    elif pais == 'IND' and pais2 == 'CHN':
        scene bg ind_chn
        "Showing the chart for India and China."
    elif pais == 'IND' and pais2 == 'AUS':
        scene bg ind_aus 
        "Showing the chart for India and Australia."
    elif pais == 'IND' and pais2 == 'ECU':
        scene bg ind_ecu  
        "Showing the chart for India and Ecuador."
    else:
        "The conditions for displaying the image were not met."
    jump comment_scene  # Volver a la escena de comentarios

label comment_scene:
    # show eileen sad 
    # Escena donde el personaje comenta lo que ha visto
    "After seeing the data, the character reflects:"
    
    if co2_level > 400:
        "The data is alarming. We need to act now."
    else:
        scene bg cielolev
        "It is a relief to see that levels have not risen too much, but we must remain vigilant."

    # Volver a la habitación o reiniciar el ciclo
    "Do you want to go back to your room or leave?"
    menu:
        "Back to the room":
            jump start
        "Salir":
            "Thank you for exploring climate change. See you next time!"


label tiempo_malgastado:
    "Wasted time eventually has consequences."
    "By not informing yourself about climate change, the repercussions reach your life."
    "Te enfrentas a situaciones difíciles que podrían haberse evitado si hubieras investigado."
    
    "Ultimately, lack of preparation leads you to a tricky situation."
    "The game is over."
    
    
    menu:
        "Restart the game.":
            jump second  # Suponiendo que el inicio del juego es el label 'start'
        "Salir.":
            $ renpy.quit()
