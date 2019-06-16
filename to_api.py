import requests


class ApiRequestor():
    def __init__(self, url, auth=None):
        """
        @param auth tuple, for example ('user', 'pass') 
        """
        self.url = url
        self.auth = auth

    def sync(self, service):
        """
        Checks that service is up to date in API.
        If is needed calls create, update or delete.
        """
        existing_service = self._check_service_exist(service.name)
        if service.deleted:
            if existing_service is not None:
                self._delete(existing_service["id"])
            return

        if existing_service is None:
            service_id = self._create(service)
        else:
            service_id = existing_service["id"]
            self._update(existing_service, service)

        self._set_servers(service_id, service.servers)

    def _check_service_exist(self, service_name):
        response = requests.get(self.url + "/services", auth=self.auth)
        if response.status_code != 200:
            raise Exception("List of services cannot be fetched")

        for service_dict in response.json():
            if service_dict["name"] == service_name:
                return service_dict
        return None

    def _delete(self, service_id):
        response = requests.delete(self.url + "/services/" + str(service_id), auth=self.auth)
        if response.status_code != 204:
            raise Exception("Service cannot be deleted, status:{}".format(response.status_code))

        print("Service deleted: {}".format(service_id))

    def _create(self, service):
        """
        Creates service
        @returns service ID
        """
        response = requests.post(self.url + "/services", auth=self.auth,
                                 data=service.to_json(), allow_redirects=False)
        if response.status_code != 302:
            raise Exception("Service cannot be created, status:{}".format(response.status_code))

        print("Service created: {0.name}".format(service))

        return int(response.headers["Location"].rsplit("/", 1)[1])

    def _update(self, existing_service, service):
        if service.is_equal(existing_service):
            return

        response = requests.put(self.url + "/services/" + str(existing_service["id"]), auth=self.auth, data=service.to_json())
        if response.status_code != 200:
            raise Exception("Service cannot be updated, status:{}".format(response.status_code))

        print("Service updated: {0.name}".format(service))

    def _set_servers(self, service_id, servers):
        response = requests.get(self.url + "/services/" + str(service_id) + "/servers", auth=self.auth)
        if response.status_code != 200:
            raise Exception("Servers cannot be fetched, status:{}".format(response.status_code))
        existing_servers = response.json()

        for server in servers:
            found = False
            for existing in existing_servers:
                if server.is_equal(existing):
                    existing_servers.remove(existing)
                    found = True
                    break
            if found:
                continue
            self._create_server(service_id, server)

        for existing in existing_servers:
            self._delete_server(existing["id"])

    def _create_server(self, service_id, server):
        response = requests.post(self.url + "/services/" + str(service_id) + "/servers", auth=self.auth,
                                 data=server.to_json(), allow_redirects=False)
        if response.status_code != 302:
            raise Exception("Server cannot be created, status:{}".format(response.status_code))
        print("Server created: {0.ip}:{0.port}".format(server))

    def _delete_server(self, server_id):
        response = requests.delete(self.url + "/servers/" + str(server_id), auth=self.auth)
        if response.status_code != 204:
            raise Exception("Server cannot be deleted, status:{}".format(response.status_code))
        print("Server deleted: {}".format(server_id))
