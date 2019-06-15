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
        # zjistit jeslti je v API,
        # pokud není, vytvoriit
        # porovnat existujci službu
        # provest update
        # pripadne smazat
        # přečíst, porovnat případně smazat beckends - servery

        existing_service = self._check_service_exist(service.name)
        if service.deleted:
            if existing_service is not None:
                self._delete(existing_service["id"])
            return

        if existing_service is None:
            existing_service = self._create(service)
        else:
            self._update(existing_service, service)

        # TODO servers

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
        if response.status_code != 200:
            raise Exception("Service cannot be deleted, status:{}".format(response.status_code))

    def _create(self, service):
        """
        Creates service
        @returns service ID
        """
        response = requests.post(self.url + "/services", auth=self.auth, data=service.to_json())
        if response.status_code != 302:
            raise Exception("Service cannot be created, status:{}".format(response.status_code))
        return int(response.headers["Location"].rsplit("/", 1)[1])

    def _update(self, existing_service, service):
        if self._services_equal(existing_service, service):
            return

        response = requests.put(self.url + "/services/" + str(existing_service["id"]), auth=self.auth, data=service.to_json())
        if response.status_code != 200:
            raise Exception("Service cannot be updated, status:{}".format(response.status_code))

    def _services_equal(self, existing_service, service):
        for key in ("ip", "port", "type", "certificate_name", "network_policy"):
            if existing_service[key] != getattr(service, key):
                return False
        return True
