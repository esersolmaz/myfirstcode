import sys
import json
from thehive4py.api import TheHiveApi
from thehive4py.models import CaseObservable

api = TheHiveApi('http://10.6.5.157:9000', 'eEBuNfc36ccy2Nk4OOdv+xOGIydptbmV')

# Init the CaseObservable object
ip_observable = CaseObservable(dataType='ip',data='8.8.8.9',tlp=1,ioc=True,sighted=True,)

# Call the API
response = api.create_case_observable("84803832",ip_observable)

# Display the result
if response.status_code == 201:
    # Get response data
    observableJson = response.json()

    # Display response data
    print(json.dumps(observableJson, indent=4, sort_keys=True))
else:
    """print('Failure: {}/{}'.format(response.status_code, response.text))"""
    print("failed")
sys.exit(0)