#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from scipy import spatial
import operator
import streamlit as st


# In[42]:


path = 'D:/Documentos/BEDU/Proyecto/' 
moviesRatings = pd.read_csv(path + 'moviesRatings.csv')
vec = []
for v in moviesRatings['genres_v']:
    v = v.replace('[','')
    v = v.replace(']','')
    vec.append(list(map(int, v.split())))
moviesRatings['genres_v'] = pd.Series(vec)    
userRatings = userRatings = pd.read_csv(path+'userRatings.csv')
userRatings =userRatings.reindex(list(userRatings.index+1))
corrMatrix = pd.read_csv(path+'corrMatrix.csv')
corrMatrix = corrMatrix.set_index('title')


# In[43]:


def Recomendacion_Usuario(user_id):
    myRatings = userRatings.loc[user_id].dropna()
    myRatings.sort_values(inplace = True, ascending = False)
    simCandidates = pd.Series(dtype = 'float64')
    for i in range(0, len(myRatings.index)):
        sims = corrMatrix[myRatings.index[i]].dropna()
        sims = sims.map(lambda x: x * myRatings[i])
        simCandidates = simCandidates.append(sims)
    simCandidates.sort_values(inplace = True, ascending = False)
    simCandidates = simCandidates.groupby(simCandidates.index).sum()
    simCandidates.sort_values(inplace = True, ascending = False)
    filteredSims = simCandidates.drop(myRatings.index, errors = 'ignore')
    return filteredSims


# In[92]:


movieDict = {}
for i in range(len(moviesRatings)):
    movieDict[moviesRatings['movieId'][i]] = (moviesRatings['title'][i], moviesRatings['genres_v'][i], 
                                              moviesRatings['size'][i], moviesRatings['Rating'][i])


# In[38]:


def Distancia(a, b):
    genresA = a[1]
    genresB = b[1]
    genreDistance = spatial.distance.cosine(genresA, genresB)
    popularityA = a[2]
    popularityB = b[2]
    popularityDistance = abs(popularityA - popularityB)
    return genreDistance + popularityDistance
def Peliculas_Similares(movieID, K):
    distances = []
    for movie in movieDict:
        if (movie != movieID):
            dist = Distancia(movieDict[movieID], movieDict[movie])
            distances.append((movie, dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(K):
        neighbors.append(distances[x][0])
    return neighbors
def Recomendacion_Pelicula(movie_id):
    K = 25
    avgRating = 0
    recommendations = Peliculas_Similares(movie_id, K)
    recomendaciones = []
    for recommendation in recommendations:
        avgRating += movieDict[recommendation][3]
        recomendaciones.append([movieDict[recommendation][0], movieDict[recommendation][3]])
    rec = pd.DataFrame(recomendaciones, columns = ['Title', 'Score'])
    rec = rec.sort_values(by = ['Score']).reset_index(drop = True)
    return rec


# In[105]:


st.title('Proyecto BEDU - Sistema de Recomendacion de Peliculas')
status = st.radio('¿Eres usuario o buscas una pelicula?', ('Usuario', 'Pelicula'))
if status == 'Usuario':
    user_id = st.number_input("Por favor ingrese su numero de usuario:", min_value = 0,
                             max_value = max(list(userRatings.index)), step = 1)
    if user_id > 0:
        st.text('Hola usuario ' + str(user_id))
        st.info("Estoy buscando películas que te podrían gustar, por favor espera")
        RU = Recomendacion_Usuario(user_id)
        st.success('He encontrado algunas películas que te prodrían gustar')
        show = st.slider('Mostrar', 5, 15, value = 10)
        st.write(pd.Series(list(RU.index)).head(show))
if status == 'Pelicula':
    pel = st.text_input("Por favor dime una pelicula que te guste:").lower()
    if len(pel) > 0:
        sim = ['-']
        ind = [0]
        for k in list(movieDict.keys()):
            if (pel in movieDict[k][0].lower()): 
                sim.append(movieDict[k][0])
                ind.append(k)
        if len(sim) == 0:
            st.error("Lo siento, no encontre la pelicula que me dijiste")
        else:
            opt = st.selectbox('¿Es alguna de estas peliculas?', sim)
            if opt != '-':
                st.text(opt + ' es una excelente eleccion')
                st.info("Estoy buscando películas similares, por favor espera")
                movie_id = ind[sim.index(opt)]
                RP = Recomendacion_Pelicula(movie_id)
                st.success('He encontrado algunas películas que te prodrían gustar')
                show = st.slider('Mostrar', 5, 15, value = 10)
                st.write(RP['Title'].head(show))     


# In[ ]:




