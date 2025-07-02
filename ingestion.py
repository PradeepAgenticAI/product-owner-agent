#!/usr/bin/env python
"""Document Ingestion Script for Product Owner Agent.

This script processes documentation files and creates a vector store
for efficient retrieval by the Product Owner Agent.
"""

import os
import glob
import sys
from typing import List, Dict, Any, Optional

import dotenv
from langchain_community.document_loaders import TextLoader, UnstructuredMarkdownLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from rich.console import Console
from rich.progress import Progress, TaskID
from langchain_openai import OpenAIEmbeddings

# Load environment variables
dotenv.load_dotenv()

# Initialize console for rich text formatting
console = Console()

# Configuration
DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")
VECTORSTORE_DIR = os.path.join(os.path.dirname(__file__), "vectorstore")
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def get_document_files() -> List[str]:
    """Get all document files to be processed.

    Returns:
        List of file paths to process
    """
    markdown_files = glob.glob(os.path.join(DOCS_DIR, "**/*.md"), recursive=True)
    text_files = glob.glob(os.path.join(DOCS_DIR, "**/*.txt"), recursive=True)
    
    return markdown_files + text_files


def load_documents(file_paths: List[str], progress: Progress, task: TaskID) -> List[Any]:
    """Load documents from file paths.

    Args:
        file_paths: List of file paths to load
        progress: Progress bar instance
        task: Task ID for the progress bar

    Returns:
        List of loaded documents
    """
    documents = []
    total_files = len(file_paths)
    
    for i, file_path in enumerate(file_paths):
        try:
            # Update progress
            file_name = os.path.basename(file_path)
            progress.update(task, description=f"Loading {file_name}", completed=i)
            
            # Load based on file extension
            if file_path.endswith(".md"):
                loader = UnstructuredMarkdownLoader(file_path)
            else:  # Default to text loader
                loader = TextLoader(file_path)
                
            docs = loader.load()
            
            # Add source metadata
            for doc in docs:
                doc.metadata["source"] = file_path
                
            documents.extend(docs)
            
        except Exception as e:
            console.print(f"[yellow]Warning:[/yellow] Error loading {file_path}: {str(e)}")
    
    # Complete the progress
    progress.update(task, description="Loading complete", completed=total_files)
    
    return documents


def split_documents(documents: List[Any], progress: Progress, task: TaskID) -> List[Any]:
    """Split documents into chunks.

    Args:
        documents: List of documents to split
        progress: Progress bar instance
        task: Task ID for the progress bar

    Returns:
        List of document chunks
    """
    # Update progress description
    progress.update(task, description="Splitting documents", completed=0)
    
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""],
        length_function=len
    )
    
    # Split documents
    document_chunks = text_splitter.split_documents(documents)
    
    # Update progress
    progress.update(task, description=f"Split into {len(document_chunks)} chunks", completed=1)
    
    return document_chunks


def create_vectorstore(document_chunks: List[Any], progress: Progress, task: TaskID) -> None:
    """Create and persist the vector store.

    Args:
        document_chunks: List of document chunks to embed
        progress: Progress bar instance
        task: Task ID for the progress bar
    """
    # Update progress description
    progress.update(task, description="Creating embeddings", completed=0)
    
    # Initialize embeddings
    embeddings = OpenAIEmbeddings()
    
    # Create and persist the vector store
    vectorstore = Chroma.from_documents(
        documents=document_chunks,
        embedding=embeddings,
        persist_directory=VECTORSTORE_DIR
    )
    
    
    # Update progress
    progress.update(task, description="Vector store created and persisted", completed=1)


def main() -> None:
    """Run the document ingestion process."""
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[bold red]Error:[/bold red] OPENAI_API_KEY environment variable not set.")
        console.print("Please set it in your .env file.")
        sys.exit(1)
    
    # Get document files
    file_paths = get_document_files()
    
    if not file_paths:
        console.print("[bold yellow]Warning:[/bold yellow] No document files found in the docs directory.")
        console.print(f"Please add markdown (.md) or text (.txt) files to {DOCS_DIR}")
        sys.exit(1)
    
    console.print(f"[bold green]Found {len(file_paths)} document files to process.[/bold green]")
    
    # Create progress bars
    with Progress() as progress:
        # Define tasks
        load_task = progress.add_task("Loading documents...", total=len(file_paths))
        split_task = progress.add_task("Waiting to split documents...", total=1)
        vectorstore_task = progress.add_task("Waiting to create vector store...", total=1)
        
        # Process documents
        documents = load_documents(file_paths, progress, load_task)
        document_chunks = split_documents(documents, progress, split_task)
        create_vectorstore(document_chunks, progress, vectorstore_task)
    
    # Print completion message
    console.print("\n[bold green]✓[/bold green] Document ingestion complete!")
    console.print(f"Processed {len(file_paths)} files into {len(document_chunks)} chunks")
    console.print(f"Vector store created at: {VECTORSTORE_DIR}")
    console.print("\nYou can now run the main application:")
    console.print("[bold]python main.py[/bold]")


if __name__ == "__main__":
    main()
