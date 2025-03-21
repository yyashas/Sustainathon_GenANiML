import chromadb
import uuid
from pdf_chunk import PDFTranslator

class VectorStore:
    """
    A class to represent a vector store using ChromaDB.
    """
    def __init__(self, collection_name):
        """
        Initialize the vector store with a collection name.
        """
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient("./chroma_db")
        self.collection = self.client.create_collection(name=self.collection_name, metadata={
        "hnsw:space": "cosine"}, get_or_create=True)
        
    
    def add_documents(self, documents):
        """
        Add documents to the vector store.
        """


        ids = []

        for i in range(len(documents)):
            ids.append(str(uuid.uuid4()))

        
        # insert documents into the collection
        self.collection.add(
            documents=documents,
            ids=ids)

        print("Documents added to the vector store.")

    def query_db(self, query, n_res = 3):
        """
        Query the vector store.
        """
        results = self.collection.query(query_texts=query, n_results=n_res)
        return results
    
    def delete_collection(self, collection_name = None):
        if collection_name is None:
            return "Please provide a collection name to delete."
        else:
            self.client.delete_collection(collection_name)
    

if __name__ == "__main__":
    # Example usage
    translator = PDFTranslator()

    # kerala_vector_store = VectorStore(collection_name="kerala_knowledge_base")
    # chunks = translator.process_pdf("source/kerala.pdf", lang="eng", translate=False, src_lang="en", dest_lang="en")
    # for _, chunk in chunks:
    #     kerala_vector_store.add_documents(chunk)
    # print("Kerala vector store populated.")


    # karnataka_vector_store = VectorStore(collection_name="karnataka_knowledge_base")
    # ktaka_coll = karnataka_vector_store.client.get_collection("karnataka_knowledge_base")
    # chunks = translator.process_pdf("karnataka.pdf", lang="kan", translate=True, src_lang="kn", dest_lang="en")
    # print(chunks)
    # for _, chunk in chunks:
    #     ktaka_coll.add(
    #         documents=chunk,
    #         ids=[str(uuid.uuid4())]
    #     )
    # print("Karnataka vector store populated.")

    # tamilnadu_vector_store = VectorStore(collection_name="tamilnadu_knowledge_base")
    # chunks = translator.process_pdf("source/tamil-nadu.pdf", "tam", translate=True, src_lang="ta", dest_lang="en")
    # for _, chunk in chunks:
    #     tamilnadu_vector_store.add_documents(chunk)
    # print("Tamil Nadu vector store populated.")


    telangana_vector_store = VectorStore(collection_name="telangana_knowledge_base")
    chunks = translator.process_pdf("source/telangana.pdf", "eng", translate=False, src_lang="te", dest_lang="en")
    print(chunks)
    for _, chunk in chunks:
        telangana_vector_store.add_documents(chunk)












