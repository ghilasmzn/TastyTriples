from SPARQLWrapper import SPARQLWrapper, POST
from colorama import Fore, Style
import subprocess
import requests
import time
import json

class FusekiLoader:
    def __init__(self, dataset_url):
        self.dataset_url = dataset_url
        self.fuseki_path = '../../apache-jena-fuseki-4.10.0/fuseki-server'
        self.server_process = None

    def is_running(self):
        response = requests.get(self.dataset_url)
        return response.status_code == 200

    def start_server(self):
        command = [self.fuseki_path]
        self.server_process = subprocess.Popen(command)
        time.sleep(5)

    def stop_server(self):
        if self.server_process and self.server_process.poll() is None:
            self.server_process.terminate()
            self.server_process.wait()
            print('Server stopped.')
    
    def load_data(self, data, graph_uri=None, content_type='text/turtle'):
        sparql = SPARQLWrapper(self.dataset_url + "/data")
        sparql.setMethod(POST)
        sparql.addParameter('Content-Type', content_type)
        if graph_uri:
            sparql.addParameter('graph-uri', graph_uri)
        sparql.setQuery(data)
        sparql.query()

    def load_data_from_file(self, file_path, content_type='text/turtle'):
        with open(file_path, 'r', encoding='utf-8') as file:
            rdf_data = file.read()

        rdf_data_encoded = rdf_data.encode('utf-8')

        headers = {'Content-Type': content_type}
        response = requests.post(f'{self.dataset_url}/data', data=rdf_data_encoded, headers=headers)

        if response.status_code == 200:
            print(Fore.GREEN+'Data of ' + file_path + ' loaded successfully.'+Style.RESET_ALL)
        else:
            print(Fore.RED+f"Failed to load data of {file_path} | Status code: {response.status_code}"+Style.RESET_ALL)
            print(response.text)

    def check_uri_exist(self, uri):
      query = """
      ASK {
          VALUES ?s { <""" + uri + """>}
          ?s ?p ?o
      }
      """ 
      headers = {'Content-Type': 'application/sparql-query'}
      response = requests.post(f'{self.dataset_url}/query', data=query.encode('utf-8'), headers=headers)

      if response.status_code == 200:
          return response.json()['boolean']
      else:
          print(Fore.RED + f"Failed to check URI existence | Status code: {response.status_code}" + Style.RESET_ALL)
          print(response.text)
          return False

    def load_data_from_file_uri(self, file_path, content_type='text/turtle'):
        with open(file_path, 'r', encoding='utf-8') as file:
          rdf_data = json.load(file)  
          
        if not self.check_uri_exist(rdf_data['@id']):
          self.load_data_from_file(file_path, content_type)
        else:
          print(Fore.YELLOW + f"> URI {rdf_data['@id']} already exists." + Style.RESET_ALL)