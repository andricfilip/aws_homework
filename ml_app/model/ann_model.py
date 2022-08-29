from pydantic import BaseModel

class ANNModel(BaseModel):
    id: str
    model_name: str
    path: str
    mse: float
    auc: float
    acc: float
    


    

