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
import os


class DocsRetrieverAgent:
    """Agent that retrieves relevant documentation based on user queries."""

    def __init__(
        self,
        vectorstore_path: str,
        model_name: str = os.getenv("LLM_MODEL"),
        temperature: float = 0.7,  # Increased temperature for more creative responses
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

        # Initialize the vectorstore
        self.vectorstore = Chroma(
            persist_directory=vectorstore_path,
            embedding_function=OpenAIEmbeddings(),
        )

        # Create the LLM
        self.llm = ChatOpenAI(
            model_name=self.model_name,
            temperature=self.temperature,
        )

        # Create a custom prompt template that encourages creative generation
        template = """
        You are a helpful product owner agent that assists with product management tasks.
        You have access to product documentation including vision, roadmap, team structure, architecture, 
        deployment principles, DevOps practices, glossary, decision frameworks, templates, and product state.
        
        Use the following pieces of context to answer the user's question.
        
        If the question asks for creative content generation (like creating roadmaps, strategies, features, or stories),
        you should generate new content that aligns with the existing documentation. Be specific and detailed in your responses.
        
        For roadmaps: Include timeline, milestones, key deliverables, and dependencies.
        For features: Include description, user value, acceptance criteria, and technical considerations.
        For user stories: Follow the "As a [role], I want [goal], so that [benefit]" format with acceptance criteria.
        
        Context: {context}
        
        Question: {question}
        """
        
        QA_PROMPT = PromptTemplate(
            template=template, input_variables=["context", "question"]
        )

        # Create the retrieval QA chain
        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 5}
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_PROMPT},
            verbose=self.verbose,
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
            
        result = self.qa.invoke({"query": question})
        
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
