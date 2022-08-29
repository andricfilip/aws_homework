FROM python:3.10.4-slim
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app/
COPY . /app/

CMD ["hypercorn", "main:app", "--bind", "0.0.0.0:9091"]



# docker build -t lossless98ue/kube_ml_homework .

# docker run --name kube-homework-db -e POSTGRES_PASSWORD=postgres \
#  -e POSTGRES_DB=ml_db -d -p 5432:5432 postgres


# docker inslect kube-homework-db ->  ip address 172.17.0.2 tu adresu vide ostali kontejneri .





# docker run --name kube_ml_homework -p 9091:9091 -e PG_USERNAME=postgres \
#  -e PG_PASSWORD=postgres \
#  -e DB_NAME=ml_db \
#  -e DB_PORT=5432 \
#  -e DB_HOST=172.17.0.2   lossless98ue/kube_ml_homework


# docker run --name kube_ml_homework -p 9091:9091 -e PG_USERNAME=postgres \
#  -e PG_PASSWORD=postgres \
#  -e DB_NAME=ml_db \
#  -e DB_PORT=31131 \
#  -e DB_HOST=k8s-master.unic.kg.ac.rs   lossless98ue/kube_ml_homework


