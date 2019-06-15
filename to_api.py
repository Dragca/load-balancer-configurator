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

        service_exists = self._check_service_exist(service.name)

    def _check_service_exist(self, service_name):
        response = requests.get(self.url + "/services/", auth = self.auth)
        if response.status_code != 200:
            raise Exception("List of services cannot be fetched")

        for service_dict in response.json():
            if service_dict["name"] == service_name:
                return True
        return False