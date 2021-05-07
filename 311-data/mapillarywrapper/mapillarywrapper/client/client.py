from ..usecase import usecase
import requests


def error_response(response):
    """
    Raises errors matching the response code
    """
    print(response)

class MapClient:
    def __init__(self, YOUR_CLIENT_ID: str) -> None:
        self.CLIENT_ID = YOUR_CLIENT_ID
        self.BASE_DOMAIN = "https://a.mapillary.com/v3/map_features"

    def trafficinfo(
        self,
        lowerbbox: list,
        upperbbox: list,
        perpage: int = 1,
        layer: str = "trafficsigns",
        value=None
    ):
        bbox_list = [*lowerbbox[::-1], *upperbbox[::-1]]
        bbox = ",".join([repr(point) for point in bbox_list])
        if value is not None:
            params = (
                f"?layers={layer}&bbox={bbox}&value={value}&per_page={perpage}&"
                f"client_id={self.CLIENT_ID}&sort_by=key"
            )
        else:
            params = (
                f"?layers={layer}&bbox={bbox}&per_page={perpage}&"
                f"client_id={self.CLIENT_ID}&sort_by=key"
            )
        complete_url = self.BASE_DOMAIN + params
        print("Requesting data from Mapillary API")
        print(complete_url)
        response = requests.get(complete_url, timeout=300)
        if response.status_code != 200:
            return error_response(response)
        url_links = [response.links["first"]["url"]]
        current_link = response.links
        print("Pages found (with up to {} results per page):\n-".format(perpage), end="\r")
        i=0
        while "next" in current_link:
            next_url = current_link["next"]["url"]
            url_links.append(next_url)
            new_response = requests.get(next_url, timeout=300)
            if new_response.status_code != 200:
                return error_response(response)
            current_link = new_response.links
            i +=1
            print(i, end="\r")
        print(i + 1)
        transform_list = []
        temp_transform = usecase.Properties()
        print("Pages of results loaded:\n-", end="\r")
        for i, v in enumerate(url_links):
            temp_response = requests.get(v, timeout=300)
            temp_json = temp_response.json()
            transform_list += temp_transform.transform_json_(temp_json)
            print(i, end="\r")
        print(i + 1)
        return transform_list
