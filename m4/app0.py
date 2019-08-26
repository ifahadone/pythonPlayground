import falcon
from falcon_multipart.middleware import MultipartMiddleware
from m4.insect import flyResource
from m4.falconKM import KMResource

api =  falcon.API(middleware=[MultipartMiddleware()])

fly = flyResource(storage_path = '.')
centroid = KMResource()

api.add_route('/cluster', centroid)
api.add_route('/fly', fly)
api.add_route('/{filenama}', fly)

