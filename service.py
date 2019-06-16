import json


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

        data = {"name": self.name, "ip": self.ip, "port": self.port,
                  "type": self.type, "network_policy": self.network_policy}

        if self.certificate_name is not None:
            data["certificate_name"] = self.certificate_name

        return json.dumps({
            "data": data
        })

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
        self.servers = [Server(**server_dict) for server_dict in servers]  # [..., {ip: 10.1.15.3, port: 80, weight: 3}, ...]

    def validate(self):
        super().validate()
        if self.type == "https":
            if self.certificate_name is None or self.certificate_name == "":
                raise ValueError("Service type 'https' requires certificate name.")

    def is_equal(self, existing_service):
        for key in ("ip", "port", "type", "certificate_name", "network_policy"):
            if existing_service[key] != getattr(self, key):
                return False
        return True


class Server:
    def __init__(self, ip, port, max_fails=3, fail_timeout=3, weight=1):
        self.ip = ip
        self.port = port
        self.max_fails = max_fails
        self.fail_timeout = fail_timeout
        self.weight = weight

    def __repr__(self):
        return "Server({0.ip}:{0.port})".format(self)

    def to_json(self):
        data = {"ip": self.ip, "port": self.port, "max_fails": self.max_fails,
                "fail_timeout": self.fail_timeout, "weight": self.weight, "status": "ENABLED"}

        return json.dumps({
            "data": data
        })

    def is_equal(self, existing):
        for key in ("ip", "port", "weight", "fail_timeout", "max_fails"):
            if existing[key] != getattr(self, key):
                return False
        if existing["status"] != "ENABLED":
            return False
        return True
