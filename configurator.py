import yaml
import requests
import os

import to_api
from service import Service


if __name__ == "__main__":
    requestor = to_api.ApiRequestor("http://172.18.0.105:8088/v2", auth=('dev', 'dev'))

    for file_name in os.listdir("examples"):
        path = os.path.join("examples", file_name)
        print(path)  # TODO use logging
        if not os.path.isfile(path):
            continue
        with open(path, 'r') as stream:
            try:
                service_dict = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                continue
        try:
            service = Service.new(service_dict)
            service.validate()
            requestor.sync(service)
        except Exception as exc:
            print(exc)
