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

    def validate(self):
        if not self.name:
            raise ValueError("Missing service name.")


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

    def validate(self):
        super().validate()
        if self.service_type == "https":
            if self.certificate_name is None or self.certificate_name == "":
                raise ValueError("Service type 'https' requires certificate name.")


if __name__ == "__main__":
    with open("examples/service1.yaml", 'r') as stream:  # TODO list and run in loop
        try:
            service_dict = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    service = 