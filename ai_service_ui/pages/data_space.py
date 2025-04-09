"""Data space."""
import streamlit as st


def introduction():
    """Introduction."""
    st.header("Espacio de datos", anchor='data-spaces',divider="gray")
    st.write("""
             Los **espacios de datos** son entornos digitales diseñados para almacenar, compartir y analizar datos de manera segura y colaborativa. Permiten que diferentes organizaciones o sistemas intercambien información de forma eficiente, manteniendo la privacidad y el control sobre los datos. Este enfoque facilita la integración de fuentes de datos diversas, optimizando procesos y generando insights valiosos para la toma de decisiones. Los espacios de datos promueven la interoperabilidad, mejoran la accesibilidad y maximizan el valor de los datos al permitir su uso conjunto y compartido entre múltiples actores.

             Los **espacios de datos** ofrecen una serie de beneficios clave que los hacen esenciales para la gestión moderna de datos:

            1. **Interoperabilidad Mejorada**: Facilitan la conexión y el intercambio de datos entre diferentes sistemas, aplicaciones y organizaciones, independientemente de sus formatos o plataformas, lo que mejora la colaboración.

            2. **Acceso Seguro y Controlado**: Permiten compartir datos de manera controlada y segura, garantizando que solo las partes autorizadas tengan acceso a la información sensible, lo que refuerza la privacidad y la seguridad.

            3. **Optimización de Procesos**: Al integrar múltiples fuentes de datos, los espacios de datos permiten automatizar y optimizar procesos, reduciendo tiempos y costos operativos, y aumentando la eficiencia.

            4. **Toma de Decisiones Basada en Datos**: Al facilitar el acceso a datos actualizados y relevantes, los espacios de datos proporcionan la base necesaria para tomar decisiones informadas, mejorando la calidad de las decisiones estratégicas y operacionales.

            5. **Escalabilidad**: Permiten manejar grandes volúmenes de datos de manera eficiente, adaptándose a las necesidades crecientes de las organizaciones y a los avances tecnológicos, sin comprometer el rendimiento.

            6. **Innovación Colaborativa**: Promueven la colaboración entre diferentes actores del ecosistema, facilitando el desarrollo de nuevas soluciones y modelos de negocio basados en datos compartidos, lo que fomenta la innovación.

            En resumen, los espacios de datos no solo mejoran la eficiencia operativa, sino que también proporcionan una base sólida para la innovación, la seguridad y la colaboración en la economía digital.
             """)

def use_case():
    """Use case."""
    st.subheader("Caso de Uso: Movilidad en el Transporte Público", anchor= 'use-case')
    st.write("""
            En un mundo donde la movilidad urbana es clave para el desarrollo sostenible de nuestras ciudades, los espacios de datos emergen como una solución innovadora para conectar información de múltiples fuentes de forma segura, eficiente y colaborativa.

            Uno de los casos de uso más destacados es la predicción del tiempo de llegada de autobuses a paradas específicas. Mediante la combinación de datos en tiempo real, como información de posicionamiento de autobuses, condiciones meteorológicas y patrones históricos de tráfico, este sistema permite a los usuarios planificar sus desplazamientos con mayor precisión, reduciendo el tiempo de espera y mejorando su experiencia de viaje.

            En este caso de uso, el espacio de datos permite la optimización de los sistemas de transporte público al integrar información de GPS, sensores de tráfico, horarios planificados y condiciones meteorológicas. Esto facilita la predicción precisa y en tiempo real del tiempo de llegada de un autobús a una parada específica.""")

    st.markdown("#### 🎯Objetivos")
    st.write("""
        Los objetivos principales de este caso de uso permiten:
        - Mejorar la eficiencia del transporte público.
        - Reducir los tiempos de espera.
        - Ofrecer una experiencia más confiable a los usuarios.


        Para ello se han realizado las siguientes acciones:
        - Obtención de datasets relacionados con la movilidad.
        - Desarrollo de un modelo de predicción de llegada de un autobús a una parada concreta.
        - Creación de una API para la consulta de esta predicción.
        - Ilustración de la reducción del tiempo de espera de autobuses.
        De esta manera, a través del espacio de datos se puede disponer tanto de los datasets utilizados como de la API desarrollada.""")

    st.markdown("#### 🚀Aplicaciones")
    st.write("""
        - **Optimización de rutas y tiempos de llegada**: Los datos en tiempo real sobre el tráfico, la velocidad de los autobuses y las condiciones de la red de carreteras permiten predecir de manera más precisa los tiempos de llegada a las paradas. La API desarrollada puede consultar el tiempo que tarda un autobús en llegar al destino requerido, mejorando la puntualidad y reduciendo los tiempos de espera para los usuarios.
        - **Análisis de patrones y ajuste en tiempo real**: Gracias a los datos históricos y en tiempo real, es posible identificar patrones en el tráfico y el comportamiento de los usuarios, permitiendo ajustar de manera proactiva los tiempos de salida, la frecuencia y la distribución de los autobuses en las rutas más demandadas.
        """)
    st.markdown("#### 💡Beneficios")
    st.write("""
             - **Eficiencia operativa**: Los autobuses pueden tomar decisiones más informadas, adaptándose a condiciones cambiantes como el tráfico o la climatología, reduciendo los tiempos de inactividad y mejorando la experiencia de los usuarios.
            - **Reducción de la congestión**: Al optimizar los tiempos de llegada, se puede evitar la saturación de ciertas rutas o paradas, distribuyendo de manera más equitativa la demanda entre las diferentes opciones de transporte.
            - **Mejor experiencia del usuario**: Los pasajeros reciben información más precisa y actualizada sobre los tiempos de llegada de los autobuses, permitiéndoles planificar mejor sus desplazamientos y reduciendo la incertidumbre.""")
