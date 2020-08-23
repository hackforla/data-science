from ..usecase import usecase
import requests


def error_response(response):
    """
    Raises errors matching the response code
    """
    print(response)


class MapClient():

    def __init__(self, YOUR_CLIENT_ID: str) -> None:
        self.CLIENT_ID = YOUR_CLIENT_ID
        self.BASE_DOMAIN = 'https://a.mapillary.com/v3/map_features'

    def trafficinfo(self, lowerbbox: list, upperbbox: list,
                    perpage: int = 1, value=None):
        bbox_list = [*lowerbbox[::-1], *upperbbox[::-1]]
        bbox = (','.join([repr(point) for point in bbox_list]))
        if value:
            params = f'?layers=trafficsigns&bbox={bbox}&value={value}&per_page={perpage}&' \
                    f'client_id={self.CLIENT_ID}&sort_by=key'
        else:
            params = f'?layers=trafficsigns&bbox={bbox}&per_page={perpage}&' \
                    f'client_id={self.CLIENT_ID}&sort_by=key'
        complete_url = self.BASE_DOMAIN + params
        response = requests.get(complete_url)
        response.links['next']
        if response.status_code != 200:
            return error_response(response)
        json_dict = response.json()
        transform_json = usecase.Properties()
        return transform_json.transform_json_(json_dict)
