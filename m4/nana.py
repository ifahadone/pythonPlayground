import asyncio
from nats.aio.client import Client as NATS

import json


async def run(loop):
    print('run def run')
    nc = NATS()

    await nc.connect("nats://192.168.10.245:4444", loop = loop)

    async def resultHandler(msg):
        print('result handler')
        subject = msg.subject
        data = msg.data.decode()

        print("Result of '{subject}': \n {data}".format(
            subject=subject, data=data))

    await nc.subscribe("clusterResult", cb = resultHandler, is_async = True)

    data = { "cluster": 3, "values": [["A101",3.149276, 101.686374],["A102", 3.1492, 101.686074],["A103",3.150076,101.670374],["A104",3.139276,101.706374],["A105",3.109276,102.890374]]}

    data = json.dumps(data).encode('utf-8')

    print('publish req')
    await nc.publish("cluster", data)

    # Terminate connection to NATS.
    ##await nc.close()

if __name__ == '__main__':
    print('nana run if')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.run_forever()