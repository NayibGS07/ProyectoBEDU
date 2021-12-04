# ProyectoBEDU
Proyecto BEDU - Sistema de Recomendación de Películas
La base de datos que se va a utilizar para este proyecto es ML-25m proporcionada por Movie Lens y que es de uso libre. 
La base de datos está conformada por:
•Películas: 58,958
•Géneros: 1,621
•Usuarios: 162,541
•Calificaciones: 25,000,095
•Fecha Inicio: 09/Enero/1995
•Fecha Final: 21/Noviembre/2019
El propósito de este proyecto es implementar un Sistema de Recomendación para mejorar la experiencia de cada usuario, brindándole mejores sugerencias de películas en base a 
sus gustos.
Para este proyecto se hicieron dos modelos de recomendación.
El primero es un sistema de recomendación a usuarios, donde se implementó una matriz de correlación para detectar qué películas estaban relacionadas en base a la actividad 
de los usuarios.
El segundo modelo es un sistema de recomendación de películas utilizando un algorítmo K-Means. La métrica utilizada es una combinación entre la distancia coseno de los géneros 
de cada película y la calificación de éstas. Utilizamos como centróide cada película de la que queremos obtener la recomendación.
Para la implementación del sistema se hizo una App Web utilizando Streamlit.
