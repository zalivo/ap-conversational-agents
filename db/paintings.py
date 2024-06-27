import os
from py2neo import Graph, Node, Relationship
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

from dotenv import load_dotenv
load_dotenv('.env')

graph = Graph(
    uri=os.getenv('NEO4J_URI'), 
    user=os.getenv('NEO4J_USER'), 
    password=os.getenv('NEO4J_PASSWORD')
)

def create_graph(graph):
    # Create nodes
    try:
        gallery = Node("Gallery", name="VR Gallery")
        p1 = Node("Painting", 
            name="King Casper",
            year="1654",
            description="Legend has it that one of the three magi who came to worship the Christ child was an African. Sometimes he is called Caspar, sometimes Balthasar. Heerschop painted him without surroundings or story. He can only be identified from his expensive clothes and the jar of incense he gave as his gift. But it is the man’s face that attracts the most attention; he looks at us proudly and self-confidently.", 
            style="Oil on panel", 
            location="Berlin Museum, Berlin",
            artist="Hendrick Heerschop",
            img="http://www.wikidata.org/entity/Q94997800",
            artifacts= ["Incense Pot", "Golden Accessories", "The Doublet"]
            )

        p2 = Node("Painting", 
            name="Head of a Boy in a Turban",
            year="1635",
            description="Dou was Rembrandt's first pupil. He took up his master's idea of studying black people. The result was this endearing tronie of a young man in a fantasy costume, who looks at us over his shoulder.",
            style="Oil on panel",
            location="Hannover, Landesmuseum",
            artist="Gerrit Dou",
            img="http://www.wikidata.org/entity/Q28940972",
            artifacts=["The Turban", "The white ostrich feather", "The blue garment"]
        )

        p3 = Node("Painting",
            name="Portrait of Dom Miguel de Castro",
            year="1643",
            description="Dom Miguel de Castro makes here a powerful, serious expression. He was a member of the Congolese elite. This portrait was commissioned by the Dutch West India Company. The WIC and the Congolese rulers traded in gold an ivory, but mainly in people. This is why Dom Miguel now is seen as a controversial figure. Dom Miguel wears fashionable European clothes. This is probably the suit he had acquired in Brazil, when he had visited the Dutch colony earlier.",
            style="Oil on panel",
            location="Statensmuseum for Kunst, Copenhagen",
            artist="Jeronimus Beckx",
            img="https://open.smk.dk/artwork/iiif/KMS7", # TODO: Any resource from wikidata?
            artifacts=["The red ostrich feather", "The cavalier hat", "The gilt garment"]
        )

        p4 = Node("Painting",
            name="Portrait of Pedro Sunda",
            year="1643",
            description="Pedro Sunda holds an elephant’s tusk. Ivory was one of the Congo’s major export products. The status of these young men is unclear. Were they assistants of the noble Dom Miguel or were they enslaved?",
            style="Oil on panel",
            location="Statensmuseum for Kunst, Copenhagen",
            artist="Jeronimus Beckx",
            img="https://open.smk.dk/artwork/iiif/KMS8",
            artifacts=[
                "The ivory tusk"
            ]
        )
        p5 = Node("Painting",
            name="Portrait of Diego Bemba",
            year="1643",
            description="We know the names of these three men from the inscriptions on the backs of the paintings. This is Diego Bemba. He holds a small casket, probably a diplomatic gift. He was one of Don Miguel de Castro's servants.",
            style="Oil on panel",
            location="Statensmuseum for Kunst, Copenhagen",
            artist="Jeronimus Beckx",
            img="https://open.smk.dk/artwork/iiif/KMS9",
            artifacts=[
                "The diplomatic gift"
            ]
        )

        p1a1 = Node("Artifact",
            name="Incense Pot",
            description="The golden pot in the painting represents an incense pot, a gift for Jesus. Presented in an ornately decorated golden container and thus expressing its worth, as explained in the bible, the gold represented the kingship of Jesus. In the bible the incense was given as one of the three gifts after the birth of Jesus. The objects shown in this painting specifically is frankincense, which embodied Jesus’ deity. In the old testament frankincense was typically burnt in temples as an offering for god. With King Caspar gifting this to Jesus, he affirms that Jesus is both man and god. Additionally frankincense was thought to have healing powers, used in the east as a traditional healing method."
        )
        p1a2 = Node("Artifact",
            name="Golden Accessories", 
            description="In the painting Caspar is seen wearing different types of golden accessories. Due to its rarity and unique colour gold was often used in paintings as a form of symbolism. Gold would represent the high power and status of the wearer. The 17th century was often thought as the age of elegance when it comes to accessories. The sprinkling of jewels to show power was replaced by the wearing of a few carefully selected statement pieces to show taste. Finely carved rings, such as the one worn by King Caspar, were the preferred type of jewel worn by nobles.Additionally gold often represented the light of god in Christian art."
        )
        p1a3 = Node("Artifact",
            name="The Doublet",
            description="The man in the painting is seen wearing a yellow doublet paired with an intricately detailed and jewelled cloak. A doublet is a type of form fitted waist length jacket worn with the aims of adding shape and padding to the body, often made from linen or wool which would help keep the wearer warm. Additionally, the colour yellow was often associated with the sun and was seen as a connection to god in many religions."
        )

        p2a1 = Node("Artifact",
            name="The Turban", 
            description="A turban is a type of headwear constructed by the winding of cloth. It was often made from strong fabrics such as cotton and worn as customary headwear by people of various cultures."
        )
        p2a2 = Node("Artifact",
            name="The white ostrich feather", 
            description="The feather seen in the painting forms a type of decoration on the turban worn by the boy. The addition of elements of nature was deemed as a way of honouring culture and land. In many cultures a white feather is seen as a sign of hope or peace."
        )
        p2a3 = Node("Artifact",
            name="The blue garment", 
            description="The garment worn by the boy represents a fantasy costume, with elements from a variety of styles from 17th century clothing. During this time, the pigment blue was the most lavish and difficult to obtain. It was the colour of power and royalty and represented self-worth."
        )

        p3a1 = Node("Artifact",
            name="The red ostrich feather", 
            description="The feather Dom Miguel de Castro is shown wearing is an ostrich feather. Such feather were often seen as a symbol of elegance or luxurious extravagance. The colour red was often associated with wealth and power, due to fact that it was the first colour ever developed for painting and dyeing. The wearing of feathers on a headdress indicated a sign of status wealth and ethnicity. Often, the wearing of more rare and unusual items  would indicate a higher societal status."
        )
        p3a2 = Node("Artifact",
            name="The cavalier hat", 
            description="The cavalier hat was a commonly worn wide-brimmed hat from the 17th century. The name of this hat originates from supports of King Charles I, known as the Cavaliers, who were known for wearing extravagant garments. The hats were often made from felt and accentuated with ostrich feathers, secured on the hat with a broach. One side was often pinned to its base, creating an asymmetrical look."
        )
        p3a3 = Node("Artifact",
            name="The gilt garment", 
            description="The garment worn by Dom Miguel de Castro is ornately decorated with silver gilt embroidery, using metal threads. Silver often symbolized wealth, grace and elegance. Additionally, the garment includes a plain falling band, a commonly worn collar during the 17th century. Such bands were often made from sheer, white fabric such as linen without additional lace on the edges."
        )
        p4a1 = Node("Artifact",
            name="The ivory tusk", 
            description="Pedro Sunda is shown holding the tusk of an elephant. The material of a tusk, ivory, was deemed very valuable due to its beauty and durability, substantially exported due to its high demand. Additionally, the material was used as a way to craft objects or carve depictions, so called ivories.Throughout history, a tusk as a whole often represented strength and power." 
        )
        p5a1 = Node("Artifact",
            name="The diplomatic gift",
            description="The small casket held by Diego Bemba is assumed to be a diplomatic gift. Such gifts were given by a diplomat or leader as a courtesy when entering a foreign country. A decorative box such as the one presented in the painting, was more than a functional packaging, complemented with artistic elements."
        )

        # Create relationships
        gallery_p1 = Relationship(gallery, "HAS_PAINTING", p1)
        gallery_p2 = Relationship(gallery, "HAS_PAINTING", p2)
        gallery_p3 = Relationship(gallery, "HAS_PAINTING", p3)
        gallery_p4 = Relationship(gallery, "HAS_PAINTING", p4)
        gallery_p5 = Relationship(gallery, "HAS_PAINTING", p5)

        p1_a1 = Relationship(p1, "USES_ARTIFACT", p1a1)
        p1_a2 = Relationship(p1, "USES_ARTIFACT", p1a2)
        p1_a3 = Relationship(p1, "USES_ARTIFACT", p1a3)
        p2_a1 = Relationship(p2, "USES_ARTIFACT", p2a1)
        p2_a2 = Relationship(p2, "USES_ARTIFACT", p2a2)
        p2_a3 = Relationship(p2, "USES_ARTIFACT", p2a3)
        p3_a1 = Relationship(p3, "USES_ARTIFACT", p3a1)
        p3_a2 = Relationship(p3, "USES_ARTIFACT", p3a2)
        p3_a3 = Relationship(p3, "USES_ARTIFACT", p3a3)
        p4_a1 = Relationship(p4, "USES_ARTIFACT", p4a1)
        p5_a1 = Relationship(p5, "USES_ARTIFACT", p5a1)

        # Merge nodes and relationships into the graph
        #merge paintings
        graph.merge(gallery, "Gallery", "name")
        graph.merge(p1, "Painting", "name")
        graph.merge(p2, "Painting", "name")
        graph.merge(p3, "Painting", "name")
        graph.merge(p4, "Painting", "name")
        graph.merge(p5, "Painting", "name")

        #merge artifacts
        graph.merge(p1a1, "Artifact", "name")
        graph.merge(p1a2, "Artifact", "name")
        graph.merge(p1a3, "Artifact", "name")
        graph.merge(p2a1, "Artifact", "name")
        graph.merge(p2a2, "Artifact", "name")
        graph.merge(p2a3, "Artifact", "name")
        graph.merge(p3a1, "Artifact", "name")
        graph.merge(p3a2, "Artifact", "name")
        graph.merge(p3a3, "Artifact", "name")
        graph.merge(p4a1, "Artifact", "name")
        graph.merge(p5a1, "Artifact", "name")

        #merge relationships
        graph.merge(gallery_p1)
        graph.merge(gallery_p2)
        graph.merge(gallery_p3)
        graph.merge(gallery_p4)
        graph.merge(gallery_p5)

        graph.merge(p1_a1)
        graph.merge(p1_a2)
        graph.merge(p1_a3)
        graph.merge(p2_a1)
        graph.merge(p2_a2)
        graph.merge(p2_a3)
        graph.merge(p3_a1)
        graph.merge(p3_a2)
        graph.merge(p3_a3)
        graph.merge(p4_a1)
        graph.merge(p5_a1)

        print("Graph nodes and relationships created successfully!")
    except Exception as e:
        print(e)

def main():
    create_graph(graph)
    # print(get_all_paintings(graph).to_table())
    # print(get_all_artifacts(graph).to_table())

if __name__ == "__main__":
    main()