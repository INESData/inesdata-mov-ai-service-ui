"""Bus information."""
import json

import folium
import streamlit as st
from ai_service_ui.settings import settings
from streamlit_folium import st_folium


def get_line_map(outbound_stops:dict, inbound_stops:dict)-> folium.Map:
    """Create the map with the routes of each line.

    Args:
        outbound_stops (dict): Stops on the outbound journey
        inbound_stops (dict): Stops on the return journey

    Returns:
        folium.Map: Map of both routes
    """
    outbound_coordinates = [(stop["geometry"]["coordinates"][1], stop["geometry"]["coordinates"][0]) for stop in outbound_stops["stops"]]
    inbound_coordinates = [(stop["geometry"]["coordinates"][1], stop["geometry"]["coordinates"][0]) for stop in inbound_stops["stops"]]

    m = folium.Map(location=outbound_coordinates[0], zoom_start=14)
    folium.PolyLine(
        locations=outbound_coordinates,
        color='blue',
        weight=2
    ).add_to(m)

    for stop in outbound_stops["stops"]:
        coords = stop['geometry']['coordinates'][::-1]
        folium.CircleMarker(
            location=coords,
            radius=5,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.8,
            popup=folium.Popup(f"{stop['stop']} - {stop['name']}", max_width=300)
        ).add_to(m)

    folium.PolyLine(
        locations=inbound_coordinates,
        color='green',
        weight=2
    ).add_to(m)

    for stop in inbound_stops["stops"]:
        coords = stop['geometry']['coordinates'][::-1]
        folium.CircleMarker(
            location=coords,
            radius=5,
            color='green',
            fill=True,
            fill_color='green',
            fill_opacity=0.8,
            popup=folium.Popup(f"{stop['stop']} - {stop['name']}", max_width=300)
        ).add_to(m)

    legend_html = f"""
        <div style="
            position: fixed;
            bottom: 50px;
            left: 50px;
            background-color: white;
            border: 2px solid black;
            z-index: 9999;
            font-size: 14px;
            padding: 10px;
            border-radius: 5px;
            white-space: nowrap;
            display: inline-block;">
            <div>
                <i style="background:blue; width: 15px; height: 15px; display: inline-block; margin-right: 10px;"></i>
                {outbound_stops["name_1"]}
            </div>
            <div>
                <i style="background:green; width: 15px; height: 15px; display: inline-block; margin-right: 10px;"></i>
                {inbound_stops["name_2"]}
            </div>
        </div>
    """

    # Añadir la leyenda al mapa
    m.get_root().html.add_child(folium.Element(legend_html))


    return m

def line_information_map(line_id:str,line_information_path:str = settings.line_information_path)-> folium.Map:
    """Take the stops from both routes of a line and return the map with these stops plotted.

    Args:
        line_id (str): line id
        line_information_path (str, optional): The path of the JSON containing the stops of a specific line. Defaults to settings.line_information_path.

    Returns:
        folium.Map: Map of both routes
    """
    with open(line_information_path, "r") as file:
        lines_data = json.load(file)
    outbound_stops = next(
        filter(lambda line: line["line"] == line_id and line["direction"] == "1", lines_data),
        None
    )

    inbound_stops =  next(
        filter(lambda line: line["line"] == line_id and line["direction"] == "2", lines_data),
        None
    )
    m = get_line_map(outbound_stops,inbound_stops)
    return m

def stop_information_map(stop_information_path:str = settings.stop_information_path)-> folium.Map:
    """Create the map with all available stops.

    Args:
        line_information_path (str, optional): The path to the JSON containing the available stops. Defaults to settings.line_information_path.

    Returns:
        folium.Map: Map with stops
    """
    with open(stop_information_path, "r") as file:
        stops_data = json.load(file)

    m = folium.Map(location=[40.465, -3.689], zoom_start=15)

    for stop in stops_data:
        if len(stop['lines'])<6:
            width = 200
            height = 150
        else:
            width = 300
            height = 200
        formatted_list = ",\n".join(stop['lines'])
        popup_html = f"""
        <div style="font-size: 18px; width: {width}px; height: {height}px; padding: 10px; background-color: lightblue; border-radius: 10px;">
            <h5><b>{stop['stop']} - {stop['name']}</b></h5>
            <p>Líneas: {formatted_list}</p>
        </div>
        """

        folium.Marker(
            location=stop['geometry']['coordinates'][::-1],
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(m)

    return m


def lines_information(line_list:list=settings.line_list)-> folium.Map:
    """Selectable drawing the map for each line.

    Args:
        line_list (list, optional): line list. Defaults to settings.line_list.

    Returns:
        folium.Map: Map of both routes or None
    """
    st.selectbox("Selecciona la línea 🚍:", line_list,key="line_id")

    if st.session_state["line_id"] != "-":
        line_map = line_information_map(st.session_state["line_id"])
        return line_map
    else:
        return None


def introduction():
    """Introduction."""
    st.header("Información de líneas y paradas", anchor='stop-line-information',divider="gray")
    st.write("""
             En esta sección, se presenta un mapa interactivo donde los usuarios pueden visualizar las paradas de autobuses ubicadas en la zona de **Plaza de Castilla**. El mapa destaca únicamente aquellas paradas que están relacionadas con las rutas que pasan por esta zona. Mediante una interfaz intuitiva, se puede explorar las paradas, identificar fácilmente su ubicación y acceder a detalles adicionales sobre las líneas que las recorren.

            Esta herramienta permite a los usuarios planificar mejor sus trayectos y obtener información precisa sobre las opciones de transporte disponibles en esta área clave. """)


def stop_map_section()->str:
    """Stop map section."""
    stops_map = stop_information_map()
    st_folium(stops_map, width=700, height=500)

    # st.markdown("## Prediccion del tiempo de llegada")
    st.header("Prediccion del tiempo de llegada", anchor='bus-time-arrival',divider="gray")
    st.write("""
             En esta sección, los usuarios pueden obtener la predicción del tiempo de llegada de un autobús para una **línea y parada específicas**. Para ello, se selecciona la línea de autobús deseada. Una vez seleccionada, se desplegará un mapa interactivo que muestra el recorrido completo de la línea, destacando todas las paradas por las que transita el autobús. El usuario podrá identificar la parada de su interés en el mapa. Al seleccionar la parada, se procesará la información y se mostrará la predicción del tiempo estimado para la llegada del próximo autobús a dicha parada.

             Esta herramienta permite una consulta rápida y precisa para facilitar la planificación de los viajes en transporte público.""")
    line_map = lines_information()

    if line_map:
        st.components.v1.html(line_map._repr_html_(),  width=700, height=500)
