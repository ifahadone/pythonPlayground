from functionKM import perform
import json

def callDataKM(data):

    data = json.loads(data)
    noC = data['cluster']

    totalCoor = len(data['values'])

    result = perform(noC,data['values'])

    result = json.dumps(result)

    return result
