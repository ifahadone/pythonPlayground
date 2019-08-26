import falcon, json
import numpy as np

import io,os,uuid,mimetypes

from m4.flyDetect import detect


class flyResource(object):

    _CHUNK_SIZE_BYTES = 4096

    def __init__(self, storage_path, fopen=io.open):
        self._storage_path = storage_path
        self._fopen = fopen

    def on_get(self, req, resp, filenama):

        resp.content_type = mimetypes.guess_type(filenama)[0]
        resp.stream, resp.content_length = self.open(filenama)

        resp.status = falcon.HTTP_200
    
    def on_post(self, req, resp):

        image = req.get_param("image")
        raw = image.file.read()
        datas = np.fromstring(raw, np.uint8)
        result, noDetect, coverage = detect(datas)
        result = result.tobytes()
        result = io.BytesIO(result)

        fileName = self.save(result)
        
        output = { 
            'image URL': 'https://psdev.datumcorp.com/' + fileName,
            'filename': fileName,
            'result': noDetect,
            'coverage': coverage
        }

        resp.location = fileName
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(output)

    def save(self, fileObj):

        #ext = mimetypes.guess_extension(req.content_type)
        filenama = "{uuid}{ext}".format(uuid=uuid.uuid4(), ext='.jpg')
        image_path = os.path.join(self._storage_path, filenama)
        with open(image_path, "wb") as image_file:
            while True:
                chunk = fileObj.read(4096)
                image_file.write(chunk)
                if not chunk:
                    break

        return filenama
        
    def open(self, filenama):
        

        image_path = os.path.join(self._storage_path, filenama)
        stream = self._fopen(image_path, 'rb')
        content_length = os.path.getsize(image_path)

        return stream, content_length


