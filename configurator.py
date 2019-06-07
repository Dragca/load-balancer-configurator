import json
import yaml


class Service:
    def __init__(self, name):
        self.name = name

    @classmethod
    def new(cls, service_dict):
        """
        From definition of service in given dict 
        creates ActiveService or DeletedService instance.
        @param service_dict - dict
        @returns new instance of service
        """

        if "deleted" in service_dict and service_dict["deleted"] == True:
            return DeletedService(service_dict["name"])

        return ActiveService(**service_dict)


    def to_json(self):
        if self.deleted:
            return json.dumps({'name': self.name})

        result = {"name": self.name, "ip": self.ip, "port": self.port,
                  "type": self.type, "network_policy": self.network_policy}

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
    def __init__(self, name, ip, port, type, network_policy, certificate_name=None, servers=None):
        self.deleted = False

        super().__init__(name)
        self.ip = ip
        self.port = port
        self.type = type
        self.network_policy = network_policy
        self.certificate_name = certificate_name

    def validate(self):
        super().validate()
        if self.type == "https":
            if self.certificate_name is None or self.certificate_name == "":
                raise ValueError("Service type 'https' requires certificate name.")


if __name__ == "__main__":
    with open("examples/service1.yaml", 'r') as stream:  # TODO list and run in loop
        try:
            service_dict = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    service = Service.new(service_dict)
