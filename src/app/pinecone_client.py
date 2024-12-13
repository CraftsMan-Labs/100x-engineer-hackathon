from typing import List, Optional
from pinecone import Pinecone
from openai import OpenAI
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()


class PineconeRAG:
    """Handles RAG operations using Pinecone vector database"""

    def __init__(self):
        """
        Initialize PineconeRAG with necessary credentials and settings

        Args:
            pinecone_api_key: Pinecone API key
            environment: Pinecone environment
            index_name: Name of the Pinecone index to use
            openai_api_key: OpenAI API key for generating embeddings
        """
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = os.getenv("PINECONE_INDEX_NAME")
        self.namespace = os.getenv("PINECONE_NAMESPACE")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_client = OpenAI(api_key=self.openai_api_key)
        self.initialize()

    def initialize(self):
        """Initialize Pinecone client and connect to index"""
        pc = Pinecone(api_key=self.pinecone_api_key, region="us-east-1")
        self.index = pc.Index(self.index_name)

    def chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """
        Split text into chunks of approximately equal size

        Args:
            text: Text to split into chunks
            chunk_size: Target size of each chunk in words

        Returns:
            List of text chunks
        """
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i : i + chunk_size])
            chunks.append(chunk)

        return chunks

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using OpenAI's API

        Args:
            texts: List of text strings to generate embeddings for

        Returns:
            List of embedding vectors
        """
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small", input=texts
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            raise Exception(f"Error generating embeddings: {str(e)}")

    async def aupsert_documents(
        self,
        documents: List[str],
        metadata: Optional[List[dict]] = None,
    ):
        """Async version of upsert_documents"""
        await asyncio.to_thread(self.upsert_documents, documents, metadata)

    def upsert_documents(
        self,
        documents: List[str],
        metadata: Optional[List[dict]] = None,
    ):
        """
        Upsert documents and their embeddings into Pinecone

        Args:
            documents: List of document strings
            embeddings: List of embedding vectors for each document
            metadata: Optional list of metadata dicts for each document
        """
        # Process each document into chunks
        all_chunks = []
        chunk_metadata = []

        for i, doc in enumerate(documents):
            chunks = self.chunk_text(doc)
            all_chunks.extend(chunks)

            # Replicate metadata for each chunk if provided
            if metadata:
                chunk_metadata.extend([metadata[i]] * len(chunks))

        # Generate embeddings for all chunks
        embeddings = self.generate_embeddings(all_chunks)

        if metadata and len(chunk_metadata) != len(all_chunks):
            raise ValueError("Metadata length must match number of chunks")

        vectors = []
        for i, (chunk, emb) in enumerate(zip(all_chunks, embeddings)):
            vector = {
                "id": f"doc_{i}",
                "values": emb,
                "metadata": {
                    "text": chunk,
                    **(chunk_metadata[i] if chunk_metadata else {}),
                },
            }
            vectors.append(vector)

        self.index.upsert(vectors=vectors, namespace=self.namespace)

    def query(self, query: str, top_k: int = 5) -> List[str]:
        """
        Query Pinecone index with embedding vector

        Args:
            query_embedding: Embedding vector for the query
            top_k: Number of results to return

        Returns:
            List of matched document strings
        """
        query_embedding = self.generate_embeddings([query])[0]
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            namespace=self.namespace,
        )

        # Extract document texts from results
        documents = []
        for match in results.matches:
            if match.metadata and "text" in match.metadata:
                documents.append(match.metadata["text"])

        return documents
