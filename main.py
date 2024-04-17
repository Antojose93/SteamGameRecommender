
#librerías
from fastapi import FastAPI , Response
from fastapi.responses import HTMLResponse
import pandas as pd
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
#instanciar la aplicación

app = FastAPI()


#dataframes que se utilizan en las funciones de la API
developerDF= pd.read_parquet("data/Developer.parquet")
userForGenreDF= pd.read_parquet("data/UserForGenre.parquet")
UserDataDF= pd.read_parquet("data/UsersData.parquet")
bestDeveloperDF= pd.read_parquet("data/UsersWorstDeveloper.parquet")
DeveloperReviewsDF= pd.read_parquet("data/sentimiento_analisis.parquet")
modelo= pd.read_parquet("data/modelo_render.parquet")
similitudes = cosine_similarity(modelo.iloc[:,3:])


@app.get("/", response_class=HTMLResponse)
async def inicio():
    with open("./html/index.html", "r") as file:
        html_content = file.read()
    return Response(content=html_content, media_type="text/html")



@app.get('/developer/{desarrollador}', response_model=List[dict], name="DEVELOPER")
async def developer(desarrollador: str):
    # Filtrar el DataFrame por el desarrollador específico
    df_desarrollador = developerDF[developerDF['developer'] == desarrollador]

    # Agrupar por año y contar la cantidad de items y el contenido free
    info_por_año = df_desarrollador.groupby('year').agg(
        cantidad_items=('developer', 'count'),
        contenido_free=('free_to_play', lambda x: f"{(sum(x) / len(x) * 100):.2f}%")
    ).reset_index()

    # Retornar la información como JSON
    return info_por_año.to_dict(orient='records')




# Endpoint para obtener  `cantidad` de dinero gastado por el usuario, el `porcentaje`
# de recomendación en base a reviews.recommend y `cantidad de items`
@app.get('/userdata/{user_id}', response_model=List[dict])
async def userdata(user_id: str):
    # Filtrar el DataFrame según el user_id
    user_data = UserDataDF[UserDataDF['user_id'] == user_id]

    if len(user_data) == 0:
        return {"error": "El usuario no existe en los datos."}

    # Cantidad de dinero gastado por el usuario
    dinero_gastado = user_data['price'].sum()

    # Porcentaje de recomendación
    total_recomendaciones = user_data['recommend'].sum()
    cantidad_items = len(user_data)

    if cantidad_items == 0:
        porcentaje_recomendacion = 0
    else:
        porcentaje_recomendacion = (total_recomendaciones / cantidad_items) * 100

    # Formatear los resultados
    resultado = {
        "Usuario": user_id,
        "Dinero gastado": f"{dinero_gastado} USD",
        "% de recomendación": f"{porcentaje_recomendacion:.2f}%",
        "Cantidad de items": cantidad_items
    }

    return [resultado]






@app.get("/userforgenre/{genre}", name="USERFORGENRE")
async def UserForGenre(genre: str):
    # Filtramos por género
    data_genres = userForGenreDF[userForGenreDF['genres'].str.contains(genre)].copy()  # Copiamos el DataFrame para evitar la advertencia
    # Convertir minutos a horas y redondear a números enteros
    data_genres.loc[:, 'playtime_forever'] = (data_genres['playtime_forever'] / 60).round().astype(int)
    # Agrupamos por usuario y sumamos las horas jugadas
    data_playtime = data_genres.groupby('user_id')['playtime_forever'].sum().reset_index()
    # Obtenemos el usuario con más horas jugadas
    user = data_playtime.loc[data_playtime['playtime_forever'].idxmax()]['user_id']
    # Filtramos por usuario
    data_user = data_genres[data_genres['user_id'] == user]
    # Agrupamos por año y sumamos las horas jugadas
    data_year = data_user.groupby('release_year')['playtime_forever'].sum().reset_index()
    years = data_year.to_dict('records')
    # Obtenemos el año con más horas jugadas
    year = int(data_genres[data_genres['playtime_forever'] == data_genres['playtime_forever'].max()]['release_year'].values[0])
    
    return f"'Usuario con más horas jugadas para Género {genre}': {user}, 'Horas jugadas': {years}"








#Cuarta función
@app.get("/bestdeveloper/{year}", name = "BESTDEVELOPER")
async def UsersWorstDeveloper(year: int):
    mascara = (bestDeveloperDF['release_year'] == year)   
    df_filtered = bestDeveloperDF[mascara]
    developer_counts = df_filtered['developer'].value_counts().head(3)
 
    resultados = []
    for puesto, (developer, count) in enumerate(developer_counts.items(), start=1):                            
        resultados.append({f"Puesto {puesto}": developer})

    return resultados 



#Quinta función
@app.get("/sentimentanalysis/{year}", name="SENTIMENTANALYSIS")
async def sentiment_analysis(year: int):
    # Filtramos por año
    data_year = DeveloperReviewsDF[DeveloperReviewsDF['release_year'] == year]
    # Agrupamos por sentimiento y contamos las reseñas
    data_year = data_year.groupby('sentiment_analisis')['review'].count().reset_index()
    # Obtenemos el top 3
    sentiment = data_year.to_dict('records')
    # Inicializar contadores
    negative_count = 0
    neutral_count = 0
    positive_count = 0
    # Contar el número de reseñas con cada sentimiento
    for s in sentiment:
        if s['sentiment_analisis'] == 0:
            negative_count += s['review']
        elif s['sentiment_analisis'] == 1:
            neutral_count += s['review']
        elif s['sentiment_analisis'] == 2:
            positive_count += s['review']
    # Crear el diccionario con los contadores
    sentiment = {'Negative': negative_count, 'Neutral': neutral_count, 'Positive': positive_count}
    return {'Según el año de lanzamiento': year, 'Sentimiento': sentiment}




