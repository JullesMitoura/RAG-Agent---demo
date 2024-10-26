from qdrant_client import QdrantClient
import os

class QdrantService():
    def __init__(self):
        self.qdrant_client = QdrantClient(
            url=os.getenv("Q_DRANT_URL"), 
            api_key=os.getenv("Q_DRANT_KEY"),
        )

    def collections_verify(self):
        """Check available collections in Qdrant."""
        collections = self.qdrant_client.get_collections()
        return collections