#!/usr/bin/env python
"""Product Owner Agent - Interactive Chat Application.

This script runs the interactive chat application for the Product Owner Agent.
It allows users to ask questions about the product documentation and receive
relevant answers based on the ingested documentation.
"""

import os
import sys
import time
from typing import Dict, Any, Optional

import dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

from agents.docs_retriever_agent import DocsRetrieverAgent

# Load environment variables
dotenv.load_dotenv()

# Check for required environment variables
required_env_vars = ["OPENAI_API_KEY"]
for var in required_env_vars:
    if not os.getenv(var):
        print(f"Error: {var} environment variable not set. Please check your .env file.")
        sys.exit(1)

# Initialize console for rich text formatting
console = Console()


def initialize_agent() -> DocsRetrieverAgent:
    """Initialize the documentation retrieval agent.

    Returns:
        DocsRetrieverAgent: The initialized agent
    """
    vectorstore_path = os.path.join(os.path.dirname(__file__), "vectorstore")
    
    try:
        return DocsRetrieverAgent(
            vectorstore_path=vectorstore_path,
            model_name=os.getenv("LLM_MODEL", "gpt-3.5-turbo"),
            verbose=os.getenv("VERBOSE", "False").lower() == "true"
        )
    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        console.print(
            "\nPlease run the ingestion script first:\n"
            "[bold]python ingestion.py[/bold]\n"
        )
        sys.exit(1)


def display_welcome_message() -> None:
    """Display welcome message and instructions."""
    console.print(Panel.fit(
        "[bold blue]Product Owner Agent[/bold blue]\n\n"
        "Ask me anything about our product documentation, roadmap, team structure, or architecture.",
        title="Welcome",
        border_style="blue"
    ))
    console.print("Type [bold cyan]'exit'[/bold cyan] or [bold cyan]'quit'[/bold cyan] to end the session.\n")


def format_sources(sources: list) -> str:
    """Format source documents for display.

    Args:
        sources: List of source documents

    Returns:
        str: Formatted sources as markdown
    """
    if not sources:
        return ""
    
    formatted = "\n\n### Sources\n\n"
    for i, source in enumerate(sources[:3], 1):  # Limit to top 3 sources
        metadata = source.get("metadata", {})
        doc_name = metadata.get("source", "Unknown document")
        page = metadata.get("page", "")
        page_info = f" (page {page})" if page else ""
        
        formatted += f"{i}. **{os.path.basename(doc_name)}**{page_info}\n"
    
    return formatted


def process_query(agent: DocsRetrieverAgent, query: str) -> Dict[str, Any]:
    """Process a user query using the agent.

    Args:
        agent: The documentation retrieval agent
        query: User's query string

    Returns:
        Dict containing the response
    """
    start_time = time.time()
    
    with console.status("[bold green]Thinking..."):
        response = agent.query(query)
    
    elapsed_time = time.time() - start_time
    
    # Add source information to the answer
    answer = response["answer"]
    sources = response.get("source_documents", [])
    
    # Format the full response with sources
    full_response = answer + format_sources(sources)
    
    return {
        "answer": full_response,
        "elapsed_time": elapsed_time,
        "raw_response": response
    }


def main() -> None:
    """Run the interactive chat application."""
    display_welcome_message()
    
    # Initialize the agent
    agent = initialize_agent()
    
    # Main interaction loop
    while True:
        # Get user input
        user_input = Prompt.ask("\n[bold green]You[/bold green]")
        
        # Check for exit command
        if user_input.lower() in ["exit", "quit", "bye"]:
            console.print("\n[bold blue]Product Owner Agent:[/bold blue] Goodbye! Have a great day.")
            break
        
        # Process the query
        try:
            result = process_query(agent, user_input)
            
            # Display the response
            console.print("\n[bold blue]Product Owner Agent:[/bold blue]")
            console.print(Markdown(result["answer"]))
            
            # Optionally show processing time
            if os.getenv("SHOW_TIMING", "False").lower() == "true":
                console.print(f"\n[dim](Response generated in {result['elapsed_time']:.2f} seconds)[/dim]")
                
        except Exception as e:
            console.print(f"\n[bold red]Error:[/bold red] {str(e)}")


if __name__ == "__main__":
    main()
