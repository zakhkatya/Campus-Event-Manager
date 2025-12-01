FROM python:3.12-slim 
 
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/* 
 
WORKDIR /home/app/web 

ENV PYTHONDONTWRITEBYTECODE=1 \ 
    PYTHONUNBUFFERED=1 \ 
    PIP_DISABLE_PIP_VERSION_CHECK=1 
 
RUN apt-get update -y && apt-get install -y --no-install-recommends \ 
    build-essential  && \ 
    rm -rf /var/lib/apt/lists/* 
 
RUN pip install --upgrade pip 
 
COPY ./requirements.txt /requirements.txt 
RUN pip install --no-cache-dir -r /requirements.txt 
 
COPY ./entrypoint.sh /entrypoint.sh 
RUN chmod 0755 /entrypoint.sh 
 
CMD ["/entrypoint.sh"]