from ann import ANN_logic
from fastapi import FastAPI, File, UploadFile, Form
import pandas as pd
import json
# from database import Database 



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
async def train_model(filename: str = File(...), batch_size: int = Form(...), epochs: int = Form(...)):
    annModel = ANN_logic(file_name=filename, epochs=epochs,batch_size=batch_size)
    
    return annModel.train_model(filename,epochs, batch_size)
    # return "successful"

# @app.post("/predictValues")
# async def predict_values(model_id: str = Form(...), num_of_outputs: int = Form(...), dataset: UploadFile = File(...)):

#     path = database.get_model_path_by_id(model_id)
#     arr = ANN_logic.predict(ANN_logic.load_model(path), dataset.file, num_of_outputs)
#     # df = pd.read_csv(dataset.file)

#     # print(df.head)
#     return {"predictions": arr[:, 0].tolist()}
    # return {"predictions": "prediction !!!! "}


@app.post('/delete')
async def delete_model(model_name: str = Form(...) ):
    # try:
        
        print(model_name)
        ann = ANN_logic()
        ann.delete(model_name)
        return "Deleted "+model_name
    # except Exception as e:
    #     return "Bad request"
@app.post("/predictValues")
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

    # return jsonify(pred_dict)
    return pred_dict
