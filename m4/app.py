import falcon
from falcon_multipart.middleware import MultipartMiddleware
from m4.insect import flyResource
from m4.falconKM import KMResource
#
#
api =  falcon.API(middleware=[MultipartMiddleware()])
#
fly = flyResource(storage_path = 'storage.data')
centroid = KMResource()


app = falcon.API()

#
api.add_route('/cluster', centroid)
api.add_route('/flyDetect', flyDetect)
api.add_route('/{filenama}', fly)
#


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class ThingsResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = ('\nTwo things awe me most, the starry sky '
                     'above me and the moral law within me.\n'
                     '\n'
                     '    ~ Immanuel Kant\n\n')


# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
things = ThingsResource()

# things will handle all requests to the '/things' URL path
app.add_route('/fly', fly)
