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
        if value is not None:
            params = f'?layers=trafficsigns&bbox={bbox}&value={value}&per_page={perpage}&' \
                    f'client_id={self.CLIENT_ID}&sort_by=key'
        else:
            params = f'?layers=trafficsigns&bbox={bbox}&per_page={perpage}&' \
                    f'client_id={self.CLIENT_ID}&sort_by=key'
        complete_url = self.BASE_DOMAIN + params
        response = requests.get(complete_url)
        if response.status_code != 200:
            return error_response(response)
        url_links = [response.links['first']['url']]
        current_link = response.links
        while 'next' in current_link:
            next_url = current_link['next']['url']
            url_links.append(next_url)
            new_response = requests.get(next_url)
            if new_response.status_code != 200:
                return error_response(response)
            current_link = new_response.links
        transform_list = []
        temp_transform = usecase.Properties()
        for i, v in enumerate(url_links):
            temp_response = requests.get(v)
            temp_json = temp_response.json()
            transform_list += temp_transform.transform_json_(temp_json)
        return transform_list
        """Ignore the following lines, I will go back and delete them"""
        #response_test = response1.links
        #print(response_test)
        #json_dict = response1.json()
        #print(len(json_dict))
        #response2 = requests.get(response.links['next']['url'])
        #print(response2.links)
        #json_2 = response2.json()
        #print(len(json_2))
        #transform_json = usecase.Properties()
        #transform_list = transform_json.transform_json_(json_dict) + transform_json.transform_json_(json_2)
        # transform_json.transform_json_(json_dict)
        #return transform_list 
