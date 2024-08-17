#usa immagine base di python 
FROM python:3-alpine

#imposta la cartella di lavoro
WORKDIR /contrib_app

#copia il file requirements.txt nella dir di lavoro
COPY requirements.txt ./

#installa i requirements o le dipendeze
RUN pip install --no-cache-dir -r requirements.txt

#copia il resti dei file nella caretella di lavoro 
COPY . .

EXPOSE 8000

#comandoi per eseguire l'app
CMD ["python", "./main.py"]