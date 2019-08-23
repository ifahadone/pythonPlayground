import falcon, json
from functionKM import perform

class KMResource(object):

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        json_validate = False

        try:
            data = json.loads(req.stream.read())
            json_validate = True

        except:
            data = {}
        
        if json_validate is not True:
            resp.status = falcon.HTTP_404
            output = {
                'error': {
                    'status': 404,
                    'message': 'data incomplete'
                }
            }

        else:
            noC = data['cluster']
            totalCoor = len(data['values'])

            if noC <= 0 or noC > totalCoor:
                resp.status = falcon.HTTP_400
                output = {
                'error': {
                    'status': 400,
                    'message': 'Unsuitable number of cluster'
                }
            }
            
            else:
                result = perform(noC,data['values'])

                output = result

        resp.body = json.dumps(output)
