# TODO: MATCH STRUCTURE WITH EXISTING KNOWLEDGE GRAPH, AND LINK TO VUI SYSTEM

from neo4j import GraphDatabase
class PaintingsKnowledge:
    """
    Painting Knowledge in Neo4j knowledge graph including:
    - Paintings
    - Artifacts
    """
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

        # self.knowledge = self._driver.session()
        self.topics = [] #list of topics
        self.paintings = None
        self.artifacts = None
        self.artists = None

    @property
    def all_paintings(self):
        with self._driver.session() as session:
            paintings_query = session.run(
                "MATCH (painting:Painting) "
                "RETURN painting.name AS name, painting.info AS info"
            )   
            self.paintings = paintings_query
            return self.paintings
    @property
    def all_artists(self):
        with self._driver.session() as session:
            artists_query = session.run(
                "MATCH (painting:Painting) "
                "RETURN paiting.artist AS artist"
            )
            self.artists = artists_query
            return self.artists
    
    @property
    def all_artifacts(self):
        with self._driver.session() as session:
            artifacts = session.run(
                "MATCH (artifact:Artifact) "
                "RETURN artifact.name AS name, artifact.description AS description"
            )
            self.artifacts = artifacts
            return result

    # Specific Painting and Artifact raw information from knowledge graph,
    # painting including: name, description, style, location, artist name, list of artifacts
    # artifact including: name, description
    # TODO: could be blended with image processing input from gpt-4o
    def painting_info(self, painting_name):
        """
        Retrieve information of specific painting
        """
        with self._driver.session() as session:
            result = session.run(
                "MATCH (painting:Painting {name: $painting_name}) "
                "RETURN painting.description AS description, painting.style AS style, painting.location AS location, painting.artist AS artist, painting.artifacts AS artifacts",
                painting_name=painting_name
            )
            return result.single()
    def artifact_info(self, artifact_name):
        """
        Retrieve information of specific artifact
        """
        with self.knowledge.session() as session:
            result = session.run(
                "MATCH (artifact:Artifact {name: $artifact_name}) "
                "RETURN artifact.name AS name, artifact.description AS description",
                artifact_name=artifact_name,
            )
            return result.single()


# FIXME: --- A painting object for a custom painting ---
# class Paiting:
#     def __init__(self):
#         self.name = name
#         self.image = image