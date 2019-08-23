import falcon

from falcon_multipart.middleware import MultipartMiddleware
from insect import flyResource
from falconKM import KMResource

from natsKM import callDataKM

api =  falcon.API(middleware=[MultipartMiddleware()])

fly = flyResource(storage_path = '.')
centroid = KMResource()

api.add_route('/cluster', centroid)
api.add_route('/fly', fly)
api.add_route('/{filenama}', fly)

