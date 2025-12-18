"""
RAG Knowledge Ingestion Pipeline

This script implements a complete RAG (Retrieval-Augmented Generation) knowledge ingestion pipeline that:
- Enumerates and extracts content from documentation sites
- Processes and chunks text content
- Generates embeddings using Cohere
- Stores embeddings in Qdrant vector database
"""

import os
import logging
import argparse
from typing import List, Tuple, Optional
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse
import hashlib
import uuid


import requests
from bs4 import BeautifulSoup
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


@dataclass
class DocumentChunk:
    """Data class representing a document chunk with its embedding and metadata."""
    url: str
    title: str
    content: str
    section: str
    chunk_id: str
    embedding: Optional[List[float]] = None


class RAGKnowledgeIngestor:
    """Main class for RAG knowledge ingestion pipeline."""

    def __init__(self, reprocess=False):
        """Initialize the RAG knowledge ingestor with API clients and configuration."""
        # Load configuration from environment variables
        self.cohere_api_key = os.getenv("COHERE_API_KEY")
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        self.source_url = os.getenv("SOURCE_URL", "https://physical-humanoid-robotics-book.vercel.app/")
        self.reprocess = reprocess

        # Validate required configuration
        if not self.cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")
        if not self.qdrant_url:
            raise ValueError("QDRANT_URL environment variable is required")
        if not self.qdrant_api_key:
            raise ValueError("QDRANT_API_KEY environment variable is required")

        # Initialize clients
        self.cohere_client = cohere.Client(self.cohere_api_key)
        self.qdrant_client = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
            timeout=30
        )

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # Constants
        self.COLLECTION_NAME = "rag_embeddings"
        self.EMBEDDING_MODEL = "multilingual-22-12"  # Cohere model
        self.CHUNK_SIZE = 1000  # characters per chunk
        self.CHUNK_OVERLAP = 100  # overlap between chunks

    def get_all_urls(self, base_url: str) -> List[str]:
        """
        Discover and return all accessible URLs from the documentation site.

        Args:
            base_url: Base URL of the documentation site

        Returns:
            List of all page URLs found on the site
        """
        self.logger.info(f"Starting URL enumeration from: {base_url}")

        urls = set()
        visited = set()
        to_visit = [base_url]

        base_domain = urlparse(base_url).netloc

        while to_visit:
            current_url = to_visit.pop(0)

            if current_url in visited:
                continue

            visited.add(current_url)

            try:
                # Check if URL is from the same domain
                if urlparse(current_url).netloc != base_domain:
                    continue

                response = requests.get(current_url, timeout=10)

                # Only process successful responses with HTML content
                if response.status_code == 200 and 'text/html' in response.headers.get('content-type', ''):
                    urls.add(current_url)
                    self.logger.info(f"Discovered URL: {current_url}")

                    # Parse HTML to find additional links
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Find all links in the page
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        full_url = urljoin(current_url, href)

                        # Only add URLs from the same domain that haven't been visited
                        if (urlparse(full_url).netloc == base_domain and
                            full_url not in visited and
                            full_url not in to_visit):
                            to_visit.append(full_url)

            except requests.RequestException as e:
                self.logger.warning(f"Failed to fetch {current_url}: {str(e)}")
                continue
            except Exception as e:
                self.logger.warning(f"Error processing {current_url}: {str(e)}")
                continue

        self.logger.info(f"URL enumeration completed. Found {len(urls)} URLs.")
        return list(urls)

    def extract_text_from_url(self, url: str) -> Tuple[str, str, str]:
        """
        Extract title and text content from a single URL.

        Args:
            url: URL to extract content from

        Returns:
            Tuple of (title, section, content)
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract title
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else "No Title"

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Extract main content - try common content containers
            content_selectors = [
                'main',
                '[role="main"]',
                '.main-content',
                '.content',
                '.doc-content',
                '.markdown',
                '.container',
                'article',
                '.post-content'
            ]

            content = ""
            for selector in content_selectors:
                element = soup.select_one(selector)
                if element:
                    content = element.get_text(separator=' ', strip=True)
                    break

            # If no content found in specific containers, get body text
            if not content:
                body = soup.find('body')
                if body:
                    content = body.get_text(separator=' ', strip=True)

            # Clean up content
            content = ' '.join(content.split())  # Normalize whitespace

            # Extract section info from URL or page structure
            section = self._extract_section_from_url(url)

            self.logger.info(f"Extracted content from {url}: title='{title}', content_length={len(content)}")

            return title, section, content

        except Exception as e:
            self.logger.error(f"Error extracting content from {url}: {str(e)}")
            return "Error", "Error", ""

    def _extract_section_from_url(self, url: str) -> str:
        """Extract section information from URL path."""
        parsed = urlparse(url)
        path_parts = [part for part in parsed.path.split('/') if part]

        if len(path_parts) >= 1:
            return path_parts[0]  # First part of the path as section
        else:
            return "root"

    def chunk_text(self, content: str, max_length: int = 1000) -> List[str]:
        """
        Split content into appropriately sized chunks.

        Args:
            content: Text content to chunk
            max_length: Maximum length of each chunk in characters

        Returns:
            List of text chunks
        """
        if len(content) <= max_length:
            return [content]

        chunks = []
        start = 0

        while start < len(content):
            # Find the end of the chunk
            end = start + max_length

            # If we're not at the end, try to break at a sentence or paragraph boundary
            if end < len(content):
                # Look for sentence boundaries first
                sentence_break = content.rfind('. ', start + max_length // 2, end)
                if sentence_break != -1 and sentence_break > start:
                    end = sentence_break + 2
                else:
                    # Look for paragraph breaks
                    paragraph_break = content.rfind('\n\n', start + max_length // 2, end)
                    if paragraph_break != -1 and paragraph_break > start:
                        end = paragraph_break + 2
                    else:
                        # Just break at max_length
                        end = start + max_length

            chunk = content[start:end].strip()
            if chunk:  # Only add non-empty chunks
                chunks.append(chunk)

            start = end

        self.logger.info(f"Text chunked into {len(chunks)} pieces")
        return chunks

    def embed(self, text: str) -> List[float]:
        """
        Generate embedding vector for text using Cohere API.

        Args:
            text: Text to generate embedding for

        Returns:
            Embedding vector as a list of floats
        """
        try:
            response = self.cohere_client.embed(
                texts=[text],
                model=self.EMBEDDING_MODEL,
                input_type="search_document"  # Optimize for search
            )

            if response.embeddings and len(response.embeddings) > 0:
                return response.embeddings[0]
            else:
                raise Exception("No embeddings returned from Cohere API")

        except Exception as e:
            self.logger.error(f"Error generating embedding for text: {str(e)}")
            raise

    def create_collection(self, collection_name: str):
        """
        Create a vector collection in Qdrant.

        Args:
            collection_name: Name of the collection to create
        """
        try:
            # Check if collection already exists
            collections = self.qdrant_client.get_collections()
            existing_collection_names = [c.name for c in collections.collections]

            if collection_name in existing_collection_names:
                self.logger.info(f"Collection '{collection_name}' already exists")
                return

            # Get embedding dimension by creating a test embedding
            test_embedding = self.embed("test")
            embedding_size = len(test_embedding)

            # Create the collection
            self.qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=embedding_size,
                    distance=Distance.COSINE
                )
            )

            self.logger.info(f"Created collection '{collection_name}' with {embedding_size}-dimension vectors")

        except Exception as e:
            self.logger.error(f"Error creating collection '{collection_name}': {str(e)}")
            raise

    def save_chunk_to_qdrant(self, chunk: DocumentChunk):
        """
        Store a document chunk with its embedding in Qdrant.

        Args:
            chunk: DocumentChunk object to store
        """
        try:
            if chunk.embedding is None:
                raise ValueError("Chunk must have an embedding before saving to Qdrant")

            # Prepare the payload with metadata
            payload = {
                "url": chunk.url,
                "title": chunk.title,
                "content": chunk.content,
                "section": chunk.section,
                "chunk_id": chunk.chunk_id
            }

            # Check if point already exists (for duplicate prevention)
            if not self.reprocess:
                try:
                    existing_point = self.qdrant_client.retrieve(
                        collection_name=self.COLLECTION_NAME,
                        ids=[chunk.chunk_id]
                    )
                    if existing_point:
                        self.logger.info(f"Chunk {chunk.chunk_id} already exists, skipping")
                        return
                except:
                    # If retrieve fails, continue with upsert
                    pass

            # Upsert the point to Qdrant
            self.qdrant_client.upsert(
                collection_name=self.COLLECTION_NAME,
                points=[
                    models.PointStruct(
                        id=chunk.chunk_id,
                        vector=chunk.embedding,
                        payload=payload
                    )
                ]
            )

            self.logger.info(f"Saved chunk to Qdrant: {chunk.chunk_id}")

        except Exception as e:
            self.logger.error(f"Error saving chunk {chunk.chunk_id} to Qdrant: {str(e)}")
            raise

    def process_documentation_site(self):
        """
        Main orchestration function that processes the entire documentation site.
        """
        self.logger.info("Starting RAG knowledge ingestion pipeline")

        # Step 1: Create the collection
        self.logger.info("Creating Qdrant collection...")
        self.create_collection(self.COLLECTION_NAME)

        # Step 2: Get all URLs from the documentation site
        self.logger.info("Discovering URLs...")
        urls = self.get_all_urls(self.source_url)

        if not urls:
            self.logger.warning("No URLs found to process")
            return

        # Step 3: Process each URL
        for i, url in enumerate(urls):
            self.logger.info(f"Processing URL {i+1}/{len(urls)}: {url}")

            try:
                # Extract content from URL
                title, section, content = self.extract_text_from_url(url)

                if not content or len(content) < 50:  # Minimum content quality check
                    self.logger.warning(f"Content too short or empty for {url}, skipping")
                    continue

                # Chunk the content
                chunks = self.chunk_text(content, self.CHUNK_SIZE)

                # Process each chunk
                for j, chunk_text in enumerate(chunks):
                    # Create a chunk ID
                    chunk_id = self._generate_chunk_id()

                    # Create document chunk
                    doc_chunk = DocumentChunk(
                        url=url,
                        title=title,
                        content=chunk_text,
                        section=section,
                        chunk_id=chunk_id
                    )

                    # Generate embedding
                    self.logger.info(f"Generating embedding for chunk {j+1}/{len(chunks)} of {url}")
                    doc_chunk.embedding = self.embed(chunk_text)

                    # Save to Qdrant
                    self.save_chunk_to_qdrant(doc_chunk)

            except Exception as e:
                self.logger.error(f"Error processing URL {url}: {str(e)}")
                continue  # Continue with next URL

        self.logger.info("RAG knowledge ingestion pipeline completed successfully")

    def _generate_chunk_id(self) -> str:
        return str(uuid.uuid4())



def main():
    """Main function to run the RAG knowledge ingestion pipeline."""
    parser = argparse.ArgumentParser(description='RAG Knowledge Ingestion Pipeline')
    parser.add_argument('--source-url', type=str,
                       default=os.getenv("SOURCE_URL", "https://physical-humanoid-robotics-book.vercel.app/"),
                       help='Source documentation URL to process')
    parser.add_argument('--chunk-size', type=int, default=1000,
                       help='Maximum size of text chunks in characters')
    parser.add_argument('--reprocess', action='store_true',
                       help='Reprocess documents even if they already exist in the database')

    args = parser.parse_args()

    try:
        ingestor = RAGKnowledgeIngestor(reprocess=args.reprocess)

        # Override source URL if provided
        if args.source_url:
            ingestor.source_url = args.source_url

        # Override chunk size if provided
        ingestor.CHUNK_SIZE = args.chunk_size

        ingestor.process_documentation_site()
    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()