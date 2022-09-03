from email import header
from fileinput import filename
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
import os 
import boto3
import pandas as pd
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from keras import Sequential, layers
from keras.layers import Dense
from keras.models import load_model
# from database import Database
from sklearn.model_selection import LeaveOneGroupOut, train_test_split

s3 = boto3.client("s3")
dynamo = boto3.client("dynamodb", region_name='eu-central-1')

table_name = "andric-1023-2021-dynamodb"
bucket_name = "andric-1023-2021"

class ANN_logic:
    # create model for ann with parameters
    def create_model(self, num_of_inputs, num_of_outputs):
        self.model = Sequential()
        self.model.add(Dense(num_of_inputs,activation  = 'relu',input_shape=(num_of_inputs,)))
        self.model.add(Dense(units=32,activation  = 'relu'))
        self.model.add(Dense(units= 16,activation  = 'relu'))
        self.model.add(Dense(units=1))

        self.model.compile(optimizer = 'adam', loss = "mse", metrics = ['mae'])
        

    def train_model(self, file_name, epochs, batch_size):
        try:

        
            s3.download_file(Bucket = bucket_name, Key = file_name+".csv", Filename =  file_name+".csv")

            data = pd.read_csv(file_name+".csv")
            print(data.head())
            X = data.iloc[:,0:len(data.columns) - 1]
            y = data.iloc[:,len(data.columns) - 1]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

            sc = StandardScaler()
            X_train = sc.fit_transform(X_train)
            X_test = sc.transform(X_test)
            


            self.create_model(len(data.columns) - 1, 1)

            self.model.fit(X_train, y_train, batch_size = batch_size, epochs = epochs, verbose = 0)

            metrics = self.model.evaluate(X_test, y_test)
            print(metrics)
            # save model into local storage
            self.model.save(file_name+".h5")
            s3.upload_file(Filename =  file_name + ".h5", Bucket = bucket_name, Key = file_name +".h5")
            print(metrics)

                
            self.delete_from_database(os.path.splitext(file_name)[0])
            dynamo.put_item(
                TableName = table_name,
                Item = {
                    "file_name": {"S": os.path.splitext(file_name)[0]+".csv"},
                    "mse": {"S": str(round(metrics[0],2))},
                    "mae": {"S": str(round(metrics[1],2))}
                }
            )           
            return "OK"
        except Exception as ex:
            print(ex)
            return "BadRequest"


    def predict(self, model_name,file_name):
        try:
            s3.download_file(Bucket = bucket_name, Key = model_name+".h5", Filename = model_name+".h5")
            s3.download_file(Bucket = bucket_name, Key = file_name+".csv", Filename = file_name+".csv")
        except Exception as e:
            print("Folder does not exists.")
            return 500
        
        model = load_model(model_name + ".h5")
        X_test = pd.read_csv(file_name+".csv")
        config = model.get_config()
        numInputs = config["layers"][0]["config"]["batch_input_shape"][1]
        if(X_test.shape[1] != numInputs):
            return numInputs

        return model.predict(X_test)


    # delete form s3 bucket
    def delete(self, model_name):
        try:
            self.delete_from_database(model_name)
            print(model_name)
            s3.delete_object(Bucket = bucket_name, Key = model_name+".h5")
        except Exception as e:
            print("Folder doesn't exists.")


    # delete from dynamo db
    def delete_from_database(self, model_name):
        # try:
            table = boto3.resource("dynamodb").Table(table_name)
            table.delete_item(
                Key = {"file_name": model_name+".csv"}
            )
        # except Exception as e:
        #     print("No model in database")






