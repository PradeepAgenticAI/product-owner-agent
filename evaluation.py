#!/usr/bin/env python
"""Evaluation Script for Product Owner Agent.

This script evaluates the accuracy and relevance of the Product Owner Agent's
responses against a golden dataset of questions and expected answers.
It tests knowledge across all documentation, including deployment principles,
DevOps practices, terminology, decision frameworks, and templates.
"""

import json
import os
import sys
from typing import Dict, List, Any, Tuple

import dotenv
import numpy as np
from rich.console import Console
from rich.table import Table

from agents.docs_retriever_agent import DocsRetrieverAgent

# Load environment variables
dotenv.load_dotenv()

# Initialize console for rich text formatting
console = Console()

# Configuration
EVAL_DATASET_PATH = os.path.join(os.path.dirname(__file__), "evaluation_dataset.json")
VECTORSTORE_DIR = os.path.join(os.path.dirname(__file__), "vectorstore")


def load_evaluation_dataset() -> List[Dict[str, Any]]:
    """Load the evaluation dataset from JSON file.

    Returns:
        List of evaluation examples
    """
    try:
        with open(EVAL_DATASET_PATH, "r", encoding="utf-8") as f:
            dataset = json.load(f)
            
        if not isinstance(dataset, list):
            console.print("[bold red]Error:[/bold red] Evaluation dataset must be a JSON array.")
            sys.exit(1)
            
        return dataset
    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] Evaluation dataset not found at {EVAL_DATASET_PATH}")
        sys.exit(1)
    except json.JSONDecodeError:
        console.print("[bold red]Error:[/bold red] Invalid JSON in evaluation dataset.")
        sys.exit(1)


def initialize_agent() -> DocsRetrieverAgent:
    """Initialize the documentation retrieval agent.

    Returns:
        DocsRetrieverAgent: The initialized agent
    """
    try:
        return DocsRetrieverAgent(
            vectorstore_path=VECTORSTORE_DIR,
            model_name=os.getenv("LLM_MODEL"),
            verbose=False
        )
    except FileNotFoundError:
        console.print(
            f"[bold red]Error:[/bold red] Vector store not found at {VECTORSTORE_DIR}. "
            "Please run ingestion.py first."
        )
        sys.exit(1)


def evaluate_example(
    agent: DocsRetrieverAgent, 
    example: Dict[str, Any]
) -> Dict[str, Any]:
    """Evaluate a single example.

    Args:
        agent: The documentation retrieval agent
        example: The evaluation example

    Returns:
        Dict containing evaluation results
    """
    question = example.get("question")
    expected_answer = example.get("expected_answer")
    expected_sources = example.get("expected_sources", [])
    
    if not question or not expected_answer:
        return {
            "error": "Invalid example: missing question or expected_answer",
            "score": 0.0
        }
    
    # Get agent's response
    response = agent.query(question)
    answer = response.get("answer", "")
    sources = [doc.get("metadata", {}).get("source", "") for doc in response.get("source_documents", [])]
    
    # Calculate relevance score using improved keyword matching and phrase detection
    # This better handles terminology from our expanded documentation
    expected_lower = expected_answer.lower()
    answer_lower = answer.lower()
    
    # Check for exact phrases (3+ word sequences) that appear in both
    expected_words = expected_lower.split()
    answer_words = answer_lower.split()
    
    # Extract phrases (3+ words) from expected answer
    expected_phrases = []
    for i in range(len(expected_words) - 2):
        expected_phrases.append(' '.join(expected_words[i:i+3]))
    
    # Count phrases from expected answer that appear in agent's answer
    phrase_matches = sum(1 for phrase in expected_phrases if phrase in answer_lower)
    phrase_score = min(1.0, phrase_matches / max(1, len(expected_phrases) * 0.5))
    
    # Traditional keyword matching
    expected_keywords = set(expected_words)
    answer_keywords = set(answer_words)
    keyword_overlap = len(expected_keywords.intersection(answer_keywords))
    keyword_score = min(1.0, keyword_overlap / max(1, len(expected_keywords) * 0.3))
    
    # Combined score with higher weight on phrase matching
    relevance_score = 0.7 * phrase_score + 0.3 * keyword_score
    
    # Calculate source accuracy
    source_matches = 0
    for expected_source in expected_sources:
        if any(expected_source in source for source in sources):
            source_matches += 1
    
    source_score = source_matches / max(1, len(expected_sources)) if expected_sources else 1.0
    
    # Combined score (70% relevance, 30% source accuracy)
    combined_score = 0.7 * relevance_score + 0.3 * source_score
    
    return {
        "question": question,
        "agent_answer": answer,
        "expected_answer": expected_answer,
        "agent_sources": sources,
        "expected_sources": expected_sources,
        "relevance_score": relevance_score,
        "source_score": source_score,
        "combined_score": combined_score
    }


def run_evaluation() -> Tuple[List[Dict[str, Any]], Dict[str, float]]:
    """Run the evaluation on the entire dataset.

    Returns:
        Tuple of (evaluation results, summary metrics)
    """
    # Load dataset
    dataset = load_evaluation_dataset()
    console.print(f"[bold green]Loaded {len(dataset)} evaluation examples.[/bold green]")
    
    # Initialize agent
    agent = initialize_agent()
    
    # Evaluate each example
    results = []
    for i, example in enumerate(dataset):
        with console.status(f"Evaluating example {i+1}/{len(dataset)}..."):
            result = evaluate_example(agent, example)
            results.append(result)
    
    # Calculate summary metrics
    relevance_scores = [r.get("relevance_score", 0.0) for r in results if "error" not in r]
    source_scores = [r.get("source_score", 0.0) for r in results if "error" not in r]
    combined_scores = [r.get("combined_score", 0.0) for r in results if "error" not in r]
    
    # Calculate documentation coverage metrics
    all_expected_sources = []
    for r in results:
        if "error" not in r and "expected_sources" in r:
            all_expected_sources.extend(r["expected_sources"])
    
    # Count unique sources and categorize by document type
    unique_sources = set(all_expected_sources)
    doc_categories = {
        "vision_strategy": sum(1 for s in unique_sources if s.startswith("00_")),
        "roadmap": sum(1 for s in unique_sources if s.startswith("01_")),
        "teams": sum(1 for s in unique_sources if s.startswith("02_")),
        "architecture": sum(1 for s in unique_sources if s.startswith("03_")),
        "deployment": sum(1 for s in unique_sources if s.startswith("04_")),
        "devops": sum(1 for s in unique_sources if s.startswith("05_")),
        "glossary": sum(1 for s in unique_sources if s.startswith("06_")),
        "decision_frameworks": sum(1 for s in unique_sources if s.startswith("07_")),
        "templates": sum(1 for s in unique_sources if s.startswith("08_"))
    }
    
    metrics = {
        "avg_relevance_score": np.mean(relevance_scores) if relevance_scores else 0.0,
        "avg_source_score": np.mean(source_scores) if source_scores else 0.0,
        "avg_combined_score": np.mean(combined_scores) if combined_scores else 0.0,
        "num_examples": len(results),
        "num_errors": sum(1 for r in results if "error" in r),
        "doc_coverage": doc_categories,
        "total_unique_sources": len(unique_sources)
    }
    
    return results, metrics


def display_results(results: List[Dict[str, Any]], metrics: Dict[str, float]) -> None:
    """Display evaluation results in a formatted table.

    Args:
        results: List of evaluation results
        metrics: Summary metrics
    """
    # Display summary metrics
    console.print("\n[bold]Evaluation Summary:[/bold]")
    
    metrics_table = Table(show_header=True, header_style="bold")
    metrics_table.add_column("Metric")
    metrics_table.add_column("Value")
    
    metrics_table.add_row("Number of Examples", str(metrics["num_examples"]))
    metrics_table.add_row("Number of Errors", str(metrics["num_errors"]))
    metrics_table.add_row("Average Relevance Score", f"{metrics['avg_relevance_score']:.2f}")
    metrics_table.add_row("Average Source Score", f"{metrics['avg_source_score']:.2f}")
    metrics_table.add_row("Average Combined Score", f"{metrics['avg_combined_score']:.2f}")
    metrics_table.add_row("Total Unique Sources", str(metrics["total_unique_sources"]))
    
    console.print(metrics_table)
    
    # Display documentation coverage metrics
    console.print("\n[bold]Documentation Coverage:[/bold]")
    
    doc_table = Table(show_header=True, header_style="bold")
    doc_table.add_column("Document Category")
    doc_table.add_column("Coverage Count")
    
    doc_coverage = metrics["doc_coverage"]
    doc_table.add_row("Vision & Strategy", str(doc_coverage["vision_strategy"]))
    doc_table.add_row("Roadmap", str(doc_coverage["roadmap"]))
    doc_table.add_row("Teams & Allocation", str(doc_coverage["teams"]))
    doc_table.add_row("Architecture & Principles", str(doc_coverage["architecture"]))
    doc_table.add_row("Deployment Principles (Sleuth)", str(doc_coverage["deployment"]))
    doc_table.add_row("DevOps Principles (Accelerate)", str(doc_coverage["devops"]))
    doc_table.add_row("Glossary of Terms", str(doc_coverage["glossary"]))
    doc_table.add_row("Decision Frameworks", str(doc_coverage["decision_frameworks"]))
    doc_table.add_row("Templates", str(doc_coverage["templates"]))
    
    console.print(doc_table)
    
    # Display detailed results
    console.print("\n[bold]Detailed Results:[/bold]")
    
    results_table = Table(show_header=True, header_style="bold")
    results_table.add_column("#")
    results_table.add_column("Question")
    results_table.add_column("Score")
    results_table.add_column("Sources Correct")
    
    for i, result in enumerate(results):
        if "error" in result:
            results_table.add_row(
                str(i+1),
                result.get("question", "N/A"),
                "ERROR",
                "N/A"
            )
        else:
            score = result.get("combined_score", 0.0)
            score_color = "green" if score >= 0.8 else "yellow" if score >= 0.5 else "red"
            
            source_score = result.get("source_score", 0.0)
            source_status = "✓" if source_score > 0.5 else "✗"
            
            results_table.add_row(
                str(i+1),
                result.get("question", "N/A")[:50] + ("..." if len(result.get("question", "")) > 50 else ""),
                f"[{score_color}]{score:.2f}[/{score_color}]",
                source_status
            )
    
    console.print(results_table)


def main() -> None:
    """Run the evaluation script."""
    console.print("[bold]Product Owner Agent - Evaluation[/bold]\n")
    
    # Run evaluation
    results, metrics = run_evaluation()
    
    # Display results
    display_results(results, metrics)
    
    # Save results to file
    output_path = os.path.join(os.path.dirname(__file__), "evaluation_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"results": results, "metrics": metrics}, f, indent=2)
    
    console.print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
