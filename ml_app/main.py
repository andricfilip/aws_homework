from ann import ANN_logic
from fastapi import FastAPI, File, UploadFile, Form



ALLOWED_EXTENSIONS = {'txt', 'pdf', 'csv', 'xlsx'}

app = FastAPI()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.post("/trainModel/{file_name}/{batch_size}/{epochs}") # dekorator
async def train_model(file_name: str, batch_size: int, epochs: int):
    annModel = ANN_logic()
    
    return annModel.train_model(file_name,epochs, batch_size)


@app.post('/delete/{model_name}')
async def delete_model(model_name: str):
    try:
        print(model_name)
        ann = ANN_logic()
        ann.delete(model_name)
        return "Deleted "+model_name
    except Exception as e:
        return "Bad request"
@app.post("/predictValues/{model_name}/{dataset_name}")
def predict(model_name: str, dataset_name: str):
    print("Prediction")
    ann = ANN_logic()
    predictions = ann.predict(model_name, dataset_name)

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

    return pred_dict
