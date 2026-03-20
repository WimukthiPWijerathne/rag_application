from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams,Distance,PointStruct

class QdrantStorage:
    def __init__(self,url="http://localhost:6333",collection="docs",dim=3072):
        self.client=QdrantClient(url=url,timeout=30)
        self.collection=collection
        if not self.client.collection_exists(collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=dim,distance=Distance.COSINE)
            )

    def upsert(self,ids,vectors,payloads):
        points= [PointStruct(id=ids[i],vector=vectors[i],payload=payloads[i]) for i in range(len(ids))]
        self.client.upsert(self.collection,points=points)

    def search(self, query_vector, top_k: int = 5):
        results = self.client.search(
            collection_name=self.collection,
            with_payload=True,
            query_vector=query_vector,
            limit=top_k
        )
        contexts = []
        sources = set()  ##make this as a set to make sure there are no any duplicates

        for r in results:
            payload = getattr(r,"payload",{}) ##if r.payload is exist use it otherwise use empty dict
            text = payload.get("text","")
            source = payload.get("source","")
            if text:
                contexts.append(text)
                sources.add(source)
        return {"contexts": contexts, "sources": list(sources)}