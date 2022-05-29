from typing import List, Union

from fastapi import FastAPI
from pydantic import BaseModel

from neuro_comma_master.src.neuro_comma.cache import ModelCache

app = FastAPI()

class Data(BaseModel):
    data: Union[str, List[str]]


class InputData(Data):
    class Config:
        schema_extra = {
            "example": {
                "data": ("Сделать модель восстановления знаков "
                         "препинания у текста который будет получен "
                         "с помощью Speech-to-Text сервиса")
            }
        }


class OutputData(Data):
    class Config:
        schema_extra = {
            "example": {
                "data": ("Сделать модель восстановления знаков "
                         "препинания у текста, который будет получен "
                         "с помощью Speech-to-Text сервиса")
            }
        }


@app.post("/", response_model=OutputData)
async def punctuation_restoration(input: InputData):
    model = ModelCache().model
    data = input.data
    if isinstance(data, str):
        output_data = model(data)
    else:
        output_data = [model(text) for text in data]  # type: ignore
    return {"data": output_data}


@app.post("/clear_commas", response_model=OutputData)
async def remove_comas_punctuation_restoration(input: InputData):
    model = ModelCache().model
    data = input.data
    if isinstance(data, str):
        output_data = model(data.replace(',', ''))
    else:
        output_data = [model(text.replace(',', '')) for text in data]  # type: ignore
    return {"data": output_data}

def get_punctuation_restoration(data):
    model = ModelCache().model
    if isinstance(data, str):
        output_data = model(data)
    else:
        output_data = [model(text) for text in data]  # type: ignore
    return output_data

if __name__ == "__main__":

    print(get_punctuation_restoration('как можно заметить у нашей модели есть ряд преимуществ кроме того что она идеально расставила знаки препинания так она не приводит весь текст в нижний регистр в отличии от модели из найденного репозитория и так в целом во многих текстах'))
