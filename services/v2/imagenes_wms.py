from PIL import Image
import os

class maestra_imagenes:
    
    def __init__(self, imagen, ruta_imagen, empresa, ruta_img_def):
        self.imagen = imagen
        self.ruta_imagen = ruta_imagen
        self.empresa = empresa
        self.ruta_img_def = ruta_img_def
        
    def cambio_extension(self):
        img_origen = f"{self.ruta_imagen}\\{self.imagen}"
        img = Image.open(img_origen)
        name_image = str(self.imagen).replace('.jpg', '').replace('.png', '').replace('.gif', '').replace('.svg', '').replace('.jpeg', '')
        img.save(f'{self.ruta_img_def}{name_image}.jpg', quality=95)
        os.remove(img_origen)
        return name_image
