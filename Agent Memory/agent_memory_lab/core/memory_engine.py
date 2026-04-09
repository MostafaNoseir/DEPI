from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from datetime import datetime

class BaseMemory:
    def __init__(self, collection_name, persist_dir):
        self.embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
        )

        self.vector_db = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=persist_dir
        )
        
    def save(self, text):
        self.vector_db.add_texts([text])

    def search(self, query, k=2):
        results = self.vector_db.similarity_search(query, k=k)
        return [res.page_content for res in results]

class SemanticMemory(BaseMemory):
    def __init__(self):
        super().__init__(
            collection_name="semantic_memory",
            persist_dir="./chroma_semantic"
        )

class EpisodicMemory(BaseMemory):
    def __init__(self):
        super().__init__(
            collection_name="episodic_memory",
            persist_dir="./chroma_episodic"
        )

    def save_event(self, text):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event = f"[{timestamp}] {text}"
        self.save(event)