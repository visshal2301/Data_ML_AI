import os
import glob
from dotenv import load_dotenv
from typing import List, Optional

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# Load environment variables (e.g., OPENAI_API_KEY)
load_dotenv()

class RAGPipeline:
    """
    A modular RAG Pipeline to handle document processing, embedding, and semantic search.
    """
    def __init__(self, docs_dir: str = "./docs", vector_db_dir: str = "./Vector"):
        self.docs_dir = docs_dir
        self.vector_db_dir = vector_db_dir
        
        # Initialize Models
        # Note: adjust model name based on your deployment (e.g. gpt-3.5-turbo or gpt-4o)
        self.embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    def get_existing_sources(self) -> set:
        """
        Retrieves the list of 'source' filenames already present in the vector DB.
        """
        if not os.path.exists(self.vector_db_dir):
            return set()
            
        vectorstore = Chroma(
            persist_directory=self.vector_db_dir,
            embedding_function=self.embedding_model
        )
        
        # Access the underlying Chroma collection
        collection = vectorstore._collection
        if collection is None:
            return set()
            
        results = collection.get(include=["metadatas"])
        metadatas = results.get("metadatas", [])
        
        # Extract unique sources
        existing_sources = set()
        for meta in metadatas:
            if meta and "source" in meta:
                existing_sources.add(meta["source"])
                
        return existing_sources

    def process_and_chunk_documents(self):
        """
        Step 1: Read PDFs 1 by 1 from the docs folder, add specific metadata, 
        and split them into manageable chunks. Skip files already in DB.
        """
        print(f"[*] Step 1: Processing documents from '{self.docs_dir}'...")
        pdf_files = glob.glob(os.path.join(self.docs_dir, "*.pdf"))
        
        if not pdf_files:
            print(f"Warning: No PDF files found in {self.docs_dir}")
            return []
            
        existing_sources = self.get_existing_sources()
        if existing_sources:
            print(f"[*] Found {len(existing_sources)} files already in database: {', '.join(existing_sources)}")
            
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        all_chunks = []
        
        for pdf_path in pdf_files:
            file_name = os.path.basename(pdf_path)
            
            if file_name in existing_sources:
                print(f"  -> Skipping {file_name} (already in DB)")
                continue
                
            print(f"  -> Loading {file_name}")
            
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            
            # Update Document Metadata
            for doc in docs:
                # We completely override the metadata here as requested
                doc.metadata = {
                    "source": file_name,
                    "developer": "Microsoft"
                }
                
            # Split Document
            chunks = splitter.split_documents(docs)
            all_chunks.extend(chunks)
            
        print(f"[*] Total chunks created: {len(all_chunks)}")
        return all_chunks

    def store_in_vector_db(self, chunks):
        """
        Step 2: Add the chunks to a local Chroma Vector DB.
        """
        if not chunks:
            print("[*] Step 2 Skipped: No chunks to add to the database.")
            return None
            
        print(f"[*] Step 2: Saving to Chroma DB at '{self.vector_db_dir}'...")
        # Since Chroma in newer Langchain throws a deprecation warning, 
        # using the standard community integration here as imported.
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding_model,
            persist_directory=self.vector_db_dir
        )
        return vectorstore
        
    def semantic_search(self, query: str, k: int = 3) -> str:
        """
        Step 3: Query the Vector DB, get context, and talk to the LLM for a final response.
        """
        print(f"\n[*] Step 3: Searching and generating response for \n    Query: '{query}'")
        
        # Load the existing Database
        vectorstore = Chroma(
            persist_directory=self.vector_db_dir,
            embedding_function=self.embedding_model
        )
        
        # Fetch Context from Vector DB
        context_docs = vectorstore.similarity_search(query, k=k)
        
        if not context_docs:
            return "No relevant context found in the database."
            
        # Combine the page content of all retrieved chunks
        #context_text = "\n\n".join([doc.page_content for doc in context_docs])
        
        # Define the prompt for the LLM
        prompt = (
            f"{query}? You can answer using the following context: {context_docs}"
        )
        
        # Get LLM response
        response = self.llm.invoke(prompt)
        return response.content

# ==========================================
# USAGE EXAMPLE 
# ==========================================
if __name__ == "__main__":
    if not os.environ.get('OPENAI_API_KEY'):
        print("Error: Please set your OPENAI_API_KEY in the .env file")
        exit(1)
        
    # Make paths relative to this script's location so it runs from anywhere
    script_dir = os.path.dirname(os.path.abspath(__file__))
    docs_path = os.path.join(script_dir, "docs")
    vector_path = os.path.join(script_dir, "Vector")
        
    # Initialize Pipeline
    pipeline = RAGPipeline(
        docs_dir=docs_path, 
        vector_db_dir=vector_path
    )
    
    # Optional: If you want to force rebuilding the database, uncomment these:
    # chunks = pipeline.process_and_chunk_documents()
    # pipeline.store_in_vector_db(chunks)
    
    # Perform Search
    my_question = "what is LakeHouse ?"
    final_answer = pipeline.semantic_search(my_question)
    
    print("\n" + "="*50)
    print("LLM RESPONSE:")
    print("="*50)
    print(final_answer)
