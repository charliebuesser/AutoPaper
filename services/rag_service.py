from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

from services.citation_query_engine_workflow import CitationQueryEngineWorkflow


class RagService:
    def __init__(self):
        self.index = None  # Instanzvariable zum Speichern des Index

    def create_index(self, content_dir_path):
        print(f"Loading documents from directory: {content_dir_path}")
        # Lädt die Dokumente aus dem angegebenen Verzeichnis
        documents = SimpleDirectoryReader(input_dir=content_dir_path).load_data()
        print(f"Loaded {len(documents)} documents.")

            # Erzeugt einen Index aus den Dokumenten
        print("Creating index from documents...")
        self.index = VectorStoreIndex.from_documents(
                documents=documents,
                embed_model=OpenAIEmbedding(model_name="text-embedding-3-small"),
            )
        print("Index successfully created.")    


    async def retrieve_rag_answer(self, query):
        w = CitationQueryEngineWorkflow()
        result = await w.run(query=query, index=self.index)
        return result
    
    def retrivie_cite(self, result):
        import re
        pattern = r'\bSource\s(\d{1,2}|100)\b'
        cite = []
        for index, node in enumerate(result.source_nodes):
            node.text
            match = re.search(pattern, node.text)
            cite.append((match.group(1), node.metadata['file_name']))
        return cite

