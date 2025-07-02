"""Documentation Retrieval Agent for Product Owner Assistant.

This module provides a specialized agent for retrieving relevant information
from product documentation based on user queries.
"""

import os
from typing import Dict, List, Any, Optional

from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_chroma import Chroma


class DocsRetrieverAgent:
    """Agent that retrieves relevant documentation based on user queries."""

    def __init__(
        self,
        vectorstore_path: str,
        model_name: str = "gpt-4",
        temperature: float = 0.0,
        verbose: bool = False,
    ):
        """Initialize the documentation retrieval agent.

        Args:
            vectorstore_path: Path to the Chroma vectorstore
            model_name: Name of the LLM model to use
            temperature: Temperature setting for the LLM
            verbose: Whether to print verbose output
        """
        self.vectorstore_path = vectorstore_path
        self.model_name = model_name
        self.temperature = temperature
        self.verbose = verbose
        
        # Initialize components
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = self._load_vectorstore()
        self.llm = ChatOpenAI(
            model_name=self.model_name,
            temperature=self.temperature,
            verbose=self.verbose
        )
        self.qa_chain = self._create_qa_chain()

    def _load_vectorstore(self) -> Chroma:
        """Load the vector store from disk.

        Returns:
            Chroma: The loaded vector store
        """
        if not os.path.exists(self.vectorstore_path):
            raise FileNotFoundError(
                f"Vector store not found at {self.vectorstore_path}. "
                "Please run ingestion.py first."
            )
        
        return Chroma(
            persist_directory=self.vectorstore_path,
            embedding_function=self.embeddings
        )

    def _create_qa_chain(self) -> RetrievalQA:
        """Create the question-answering chain.

        Returns:
            RetrievalQA: The QA chain for document retrieval
        """
        # Custom prompt template for product documentation queries
        template = """
        You are a helpful Product Owner Assistant that answers questions based on the provided documentation.
        
        Use only the context provided below to answer the question. If you don't know the answer or can't find it
        in the context, say "I don't have enough information about that in my documentation." Don't make up answers.
        
        Always cite the specific document and section where you found the information in your answer.
        
        Context: {context}
        
        Question: {question}
        
        Answer:
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 5}
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt}
        )

    def query(self, question: str) -> Dict[str, Any]:
        """Query the documentation based on user question.

        Args:
            question: The user's question about product documentation

        Returns:
            Dict containing the answer and source documents
        """
        if self.verbose:
            print(f"Querying: {question}")
            
        result = self.qa_chain.invoke({"query": question})
        
        # Format the response
        response = {
            "answer": result["result"],
            "source_documents": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in result["source_documents"]
            ]
        }
        
        return response
    
    def get_relevant_docs(self, question: str, k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve the most relevant documents for a question without generating an answer.
        
        Args:
            question: The user's question
            k: Number of documents to retrieve
            
        Returns:
            List of relevant documents with their metadata
        """
        docs = self.vectorstore.similarity_search(question, k=k)
        
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in docs
        ]
