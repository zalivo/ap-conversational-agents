
from neo4j import GraphDatabase
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

from dotenv import load_dotenv
load_dotenv('.env')

class PaintingsKnowledge:
    """
    Painting Knowledge in Neo4j knowledge graph including:
    - Paintings
    - Artifacts
    """
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(
            uri, 
            auth=(user, password)
        )
        self.info = []
    
    #Queries functions

    def get_all_paintings(self):
        print("Getting all paintings....")
        with self._driver.session() as session:
            result = session.run(
                "MATCH (p:Painting) RETURN p.name, p.description, p.style"
            )
            self.info = [dict(record) for record in result.data()]
            return self.info

    def get_all_artifacts(self):
        with self._driver.session() as session:
            result = session.run(
                "MATCH (a:Artifact) RETURN a.name, a.description"
            )
            self.info = [dict(record) for record in result.data()]
            return self.info
    def get_specific_painting(self, painting_name):
        """
        Get specific painting by name
        return: painting information in dictionary
        """
        with self._driver.session() as session:
            result = session.run(
                "MATCH (p:Painting {name: $painting_name}) RETURN p.name, p.description, p.style, p.artist, p.img, p.artifacts",
                painting_name=painting_name
            ).single()
            self.info = [dict(result.data())]
            return self.info

    def get_specific_artifact(graph, artifact_name):
        """
            Get specific artifact by name
            return: painting information in dictionary
        """
        with graph.session() as session:
            result = session.run(
                "MATCH (a:Artifact {name: $artifact_name}) RETURN a",
                artifact_name=artifact_name
            ).single()
            self.info = [dict(result.data())]
            return self.info

    def get_artifacts_by_painting(graph, painting_name):
        with graph.session() as session:
            result = session.run(
                "MATCH (p:Painting {name: $painting_name})-[:USES_ARTIFACT]->(a:Artifact) RETURN a",
                painting_name=painting_name
            )
            self.info = [dict(record.data()) for record in result]
            return self.info

    def close(self):
        """
        Close the Neo4j driver
        """
        self._driver.close()


class PaintingStorage:
    """
    Storage for paintings and artifacts
    """
    def __init__(self, storage_endpoint, token):
        self.service_client = BlobServiceClient(
            account_url=storage_endpoint,
            credential=token
        )
        self.container_name = "paintings"
        self.container_client = self.service_client.get_container_client(self.container_name)
        self.blob_list = None
        self.blob_client = None
        
    def upload_painting(self, local_file_name, painting_name):
        """
        Upload painting to Azure Blob Storage
        """
        try:
            self.blob_client = self.container_client.get_blob_client(painting_name)
            with open(local_file_name, "rb") as data:
                self.blob_client.upload_blob(data)
                return True
        except Exception as ex:
            print(f"Error uploading painting: {ex}")
            return False

    def download_painting(self, painting_name, local_file_name):
        """
        Download painting from Azure Blob Storage
        """
        try:
            self.blob_client = self.container_client.get_blob_client(painting_name)
            with open(local_file_name, "wb") as download_file:
                download_file.write(self.blob_client.download_blob().readall())
                return True
        except Exception as ex:
            print(f"Error downloading painting: {ex}")
            return False

    def delete_painting(self, painting_name):
        """
        Delete painting from Azure Blob Storage
        """
        try:
            self.blob_client = self.container_client.get_blob_client(painting_name)
            self.blob_client.delete_blob()
            return True
        except Exception as ex:
            print(f"Error deleting painting: {ex}")
            return False

    def list_paintings(self):
    
        """
        List paintings in Azure Blob Storage
        """
        try:
            blob_list = self.container_client.list_blobs()
            for blob in blob_list:
                print(blob.name)
            return blob_list
        except Exception as ex:
            print(f"Error listing paintings: {ex}")
            return None

