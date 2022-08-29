import os

# os.environ['USER'] = 'root'
# os.environ['PASSWORD'] = 'fika'
# os.environ['DB_NAME'] = 'ml'
# os.environ['PORT'] = '30008'
# os.environ['HOST'] = 'k8s-master.unic.kg.ac.rs'

# os.environ['USER'] = 'postgres'
# os.environ['PASSWORD'] = 'postgres'
# os.environ['DB_NAME'] = 'ml_db'
# os.environ['DB_PORT'] = '5432'
# os.environ['PORT'] = '8080'
# os.environ['HOST'] = 'localhost'

user = os.environ.get('PG_USERNAME',"not set")
password = os.environ.get('PG_PASSWORD',"not set")
db_name = os.environ.get('DB_NAME',"not set")
db_port = os.environ.get('DB_PORT',"not set")
db_host = os.environ.get('DB_HOST',"not set") # db host

storage_path = "model_storage"