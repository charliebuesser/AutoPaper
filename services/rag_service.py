from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

from services.citation_query_engine_workflow import CitationQueryEngineWorkflow


"""
RagService is responsible for creating an index from documents and retrieving answers using the RAG (Retrieval-Augmented Generation) approach.
        """
        Initializes the RagService with an empty index.
        """
        """
        Creates an index from documents located in the specified directory.

        Args:
            content_dir_path (str): The path to the directory containing documents.
        """
"""
class RagService:
    def __init__(self):
        self.index = None  # Instanzvariable zum Speichern des Index

    def create_index(self, content_dir_path):
        print(f"Loading documents from directory: {content_dir_path}")
        # Lädt die Dokumente aus dem angegebenen Verzeichnis
        documents = SimpleDirectoryReader(input_dir=content_dir_path).load_data()
        """
        Asynchronously retrieves an answer for the given query using the RAG approach.

        Args:
            query (str): The query for which to retrieve an answer.
        """
        Retrieves citation information from the result.

        Args:
            result: The result object containing source nodes.

        Returns:
            A list of tuples containing index and file name of each source node.
        """

        Returns:
            The result of the query processed by the RAG workflow.
        """
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
        cite = []
        for index, node in enumerate(result.source_nodes):
            cite.append((index, node.metadata['file_name']))
        return cite

