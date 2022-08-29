from fastapi import FastAPI, File, UploadFile, Form
import pandas as pd
import json
# from database import Database 
from ann_logic.ann import ANN_logic



UPLOAD_FOLDER = 'models'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv', 'xlsx'}

# database = Database.getInstance()

app = FastAPI()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get("/pathbyid/{mdoel_id}")
async def get_path_by_id(model_id: str):
    return "pathbyid -> "+model_id

@app.get('/getlist')
async def getAnnModelList():
    return "list of models "


@app.post("/trainModel") # dekorator
async def train_model(filename: str = File(...), batch_size: int = Form(...), epochs: int = Form(...), 
    dataset: UploadFile = File(...)):
    annModel = ANN_logic(file_name=filename, epochs=epochs,batch_size=batch_size)
    
    return annModel.train_model(dataset.file,epochs, batch_size)
    # return "successful"

# @app.post("/predictValues")
# async def predict_values(model_id: str = Form(...), num_of_outputs: int = Form(...), dataset: UploadFile = File(...)):

#     path = database.get_model_path_by_id(model_id)
#     arr = ANN_logic.predict(ANN_logic.load_model(path), dataset.file, num_of_outputs)
#     # df = pd.read_csv(dataset.file)

#     # print(df.head)
#     return {"predictions": arr[:, 0].tolist()}
    # return {"predictions": "prediction !!!! "}


@app.delete('/delete/{model_name}')
def delete_model(model_name: str ):
    try:
        model_name = model_name
        print(model_name)
        ANN_logic.delete(model_name)
        return "Deleted "+model_name
    except Exception as e:
        return "Bad request"

def predict(model_name: str = Form(...), dataset_name: str = Form(...)):
    print("Prediction")
    model_name = model_name
    predictions = ANN_logic.predict(model_name, dataset_name)

    print(predictions)

    if (isinstance(predictions, int)):
        if(predictions != 500):
            return "Model receives "+ str(predictions)+" inputs. The prediction file should not have an output column. Check if the file is correct."
        return "No file on s3"
    i = 1
    pred_dict = dict()
    for prediction in predictions:
        pred_dict['prediction_' + str(i)] = float(prediction[0])
        i += 1

    return jsonify(pred_dict)
