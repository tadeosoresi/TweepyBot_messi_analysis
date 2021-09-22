# TweepyBot Analisis Messi's sale to PSG
Bot que utiliza la api de Tweepy para recopilar tweets, guardarlos en MongoDB  y realizar un analisís de sentimientos.

GUIDE:
Hacer cuenta de desarrollador en https://developer.twitter.com/en/apply-for-access, para conseguir los consumer keys y tokens :)
Luego https://www.meaningcloud.com/developer/apis, MeaningCloud provee de una API para realizar analisis de sentimientos en tweets, al hacer cuenta una key se le proveera :)

ANTES!!! de intalar los requirements, crear entorno virtual e instalar manualmente GDAL y luego FIONA (los WHL) estan en el repo, proceder con los requirements.txt

EL BOT:
Especificar hashtags como argumentos en consola (sin #), setear maximo de tweets en el codigo ya que TweepyStreaming no provee documentacion sobre limites, tmb podes setear un rango de fechas.
El bot se encarga de recopilar los tweets, almacenarlos en MongoDB, analizar cada uno para asignar un sentimiento y borrar thrash tweets.

CONNECTION.py --> Clase para gestionar MongoDB y traer los datos en formato DataFrame

Thanks!

