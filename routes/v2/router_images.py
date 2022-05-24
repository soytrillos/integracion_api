import os
from shutil import rmtree
import fastapi
from typing import List
from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import FileResponse
from services.v2.imagenes_wms import maestra_imagenes

router = APIRouter()

# empresa: str = Form(), 
@router.post("/upload", tags=["Carga Datos"])
async def upload_file(files: List[UploadFile]):
    ruta_archivo = f"{os.getcwd()}/server/images/"
    for file in files:
        print(f"{ruta_archivo}{file.filename}")
        with open(f"{ruta_archivo}{file.filename}", "wb") as myfile:
            content = await file.read()
            myfile.write(content)
            myfile.close()
        
    resultado = {"filenames": [file.filename for file in files]}
    return resultado

@router.post("/images", tags=["Carga Datos"])
async def files_m(empresa: str = Form(...), imagenes: List[UploadFile] = File(...)):
    resultado = {}
    resultado = []
    ruta_archivo_temporal = fr"{os.getcwd()}\server\images\{empresa}_temp"
    ruta_archivo = fr"{os.getcwd()}\server\images\{empresa}"
    if os.path.exists(ruta_archivo) == False:
        os.mkdir(ruta_archivo)
    elif os.path.exists(ruta_archivo_temporal) == False:
        os.mkdir(ruta_archivo_temporal)

    for imagen in imagenes:
        img = str(imagen.content_type)
        if img.count('image') == 1:
            with open(fr"{ruta_archivo_temporal}\{imagen.filename}", "wb") as myfile:
                content = await imagen.read()
                myfile.write(content)
                myfile.close()
                cl_img = maestra_imagenes(imagen.filename, ruta_archivo_temporal, empresa, ruta_archivo)
                img_new = cl_img.cambio_extension()
            resultado.append({"empresa": empresa, "imagen": img_new})
        else:
            resultado.append({'Error': f'El archivo {imagen.filename}, no es una imagen'})
               
    return resultado

@router.get("/search_images/{empresa}/{imagen}", tags=["Carga Datos"])
async def s_images(empresa: str, imagen: str):
    busqueda = os.path.isfile(fr"{os.getcwd()}\server\images\{empresa}\{imagen}")
    file_img = fr"{os.getcwd()}\server\\images\{empresa}\{imagen}"
    if busqueda == True:
        return FileResponse(path=file_img)
    else:
        raise fastapi.HTTPException(
            status_code=404, detail='Imagen no existe'
        )