import json
import yaml


class Service:
    def __init__(self, name):
        self.name = name

    def to_json(self):
        if self.deleted:
            return json.dumps({'name': self.name})

        result = {"name": self.name, "ip": self.ip_address, "port": self.port,
                  "type": self.service_type, "network_policy": self.network_policy}

        if self.certificate_name is not None:
            result["certificate_name"] = self.certificate_name

        return json.dumps(result)


class DeletedService(Service):
    def __init__(self, name):
        self.deleted = True
        super().__init__(name)


class ActiveService(Service):
    def __init__(self, name, ip_address, port, service_type, network_policy, certificate_name=None):
        self.deleted = False

        super().__init__(name)
        self.ip_address = ip_address
        self.port = port
        self.service_type = service_type
        self.network_policy = network_policy
        self.certificate_name = certificate_name
