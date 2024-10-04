# Usa un'immagine Python leggera
FROM python:3.11-slim

# Imposta la directory di lavoro all'interno del container
WORKDIR /usr/src/app

# Installa i pacchetti richiesti per creare l'ambiente virtuale
RUN apt-get update && apt-get install -y \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Crea un ambiente virtuale Python in /venv
RUN python3 -m venv /venv

# Attiva l'ambiente virtuale e installa le dipendenze
COPY ./requirements.txt ./

RUN /venv/bin/pip install --upgrade pip && /venv/bin/pip install --no-cache-dir -r requirements.txt

# Copia il resto dell'applicazione nel container, ignorando venv locale
COPY . .

# Aggiungi l'ambiente virtuale al PATH
ENV PATH="/venv/bin:$PATH"

# Comando di default per eseguire l'applicazione
CMD ["python", "main.py"]
