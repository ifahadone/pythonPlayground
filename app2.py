import falcon

from falcon_multipart.middleware import MultipartMiddleware
from insect import flyResource
from falconKM import KMResource

import asyncio
import nats.aio.client

from natsKM import callDataKM

#api =  falcon.API(middleware=[MultipartMiddleware()])

#fly = flyResource(storage_path = '.')
#centroid = KMResource()

#api.add_route('/cluster', centroid)
#api.add_route('/fly', fly)
#api.add_route('/{filenama}', fly)


async def run(loop):
    print('running `run`')
    nc = NATS()

    await nc.connect("nats://192.168.10.245:4444", loop=loop)

    async def clusterHandler(msg):
        print('cluster handler')
        subject = msg.subject
            
        data = msg.data.decode()
        result = callDataKM(data)

        print(result)
        nc.publish("clusterResult", result)

    await nc.subscribe("cluster", cb = clusterHandler, is_async = True)

if __name__ == '__main__':
    print('running `main if`')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.run_forever()

