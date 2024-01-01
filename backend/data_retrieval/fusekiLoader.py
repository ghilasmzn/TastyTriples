import requests

class FusekiLoader:
    def __init__(self, dataset_url):
        self.dataset_url = dataset_url

    def load_ttl_data(self, file_path, content_type='text/turtle'):
        with open(file_path, 'r', encoding='utf-8') as file:
            rdf_data = file.read()
        rdf_data_encoded = rdf_data.encode('utf-8')  # Encode en UTF-8

        headers = {'Content-Type': content_type}
        response = requests.post(f'{self.dataset_url}/data', data=rdf_data_encoded, headers=headers)

        if response.status_code == 200:
            print('Data loaded successfully.')
        else:
            print(f'Failed to load data. Status code: {response.status_code}')
            print(response.text)
    
    


