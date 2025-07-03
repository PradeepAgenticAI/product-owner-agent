#!/usr/bin/env python
"""
Import Product State Script.

This script imports feature and story data from CSV files and updates the
product state markdown document.
"""

import csv
import os
import re
from datetime import datetime
from typing import Dict, List, Any

# Configuration
FEATURES_CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "features.csv")
STORIES_CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "stories.csv")
PRODUCT_STATE_PATH = os.path.join(os.path.dirname(__file__), "docs", "09_product_state.md")

# Ensure data directory exists
os.makedirs(os.path.join(os.path.dirname(__file__), "data"), exist_ok=True)


def read_csv_file(file_path: str) -> List[Dict[str, str]]:
    """Read data from a CSV file.

    Args:
        file_path: Path to the CSV file

    Returns:
        List of dictionaries representing rows in the CSV
    """
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} does not exist. Returning empty list.")
        return []

    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def read_markdown_file(file_path: str) -> str:
    """Read the content of a markdown file.

    Args:
        file_path: Path to the markdown file

    Returns:
        Content of the file as a string
    """
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} does not exist. Creating a new file.")
        return ""

    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def write_markdown_file(file_path: str, content: str) -> None:
    """Write content to a markdown file.

    Args:
        file_path: Path to the markdown file
        content: Content to write
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def generate_completed_features_table(features: List[Dict[str, str]]) -> str:
    """Generate a markdown table for completed features.

    Args:
        features: List of feature dictionaries

    Returns:
        Markdown table as a string
    """
    completed_features = [f for f in features if f.get('Status', '').lower() == 'completed']
    
    if not completed_features:
        return "No completed features yet.\n"
    
    table = "| Feature ID | Feature Name | Description | Completion Date | Related Stories |\n"
    table += "|------------|-------------|-------------|----------------|----------------|\n"
    
    for feature in completed_features:
        feature_id = feature.get('FeatureID', '')
        name = feature.get('Name', '')
        description = feature.get('Description', '')
        completion_date = feature.get('CompletionDate', '')
        related_stories = feature.get('RelatedStories', '')
        
        table += f"| {feature_id} | {name} | {description} | {completion_date} | {related_stories} |\n"
    
    return table


def generate_in_progress_features_table(features: List[Dict[str, str]]) -> str:
    """Generate a markdown table for in-progress features.

    Args:
        features: List of feature dictionaries

    Returns:
        Markdown table as a string
    """
    in_progress_features = [f for f in features if f.get('Status', '').lower() == 'in progress']
    
    if not in_progress_features:
        return "No in-progress features.\n"
    
    table = "| Feature ID | Feature Name | Description | Target Completion | Progress (%) | Related Stories |\n"
    table += "|------------|-------------|-------------|-------------------|--------------|----------------|\n"
    
    for feature in in_progress_features:
        feature_id = feature.get('FeatureID', '')
        name = feature.get('Name', '')
        description = feature.get('Description', '')
        target_completion = feature.get('TargetCompletion', '')
        progress = feature.get('Progress', '0')
        related_stories = feature.get('RelatedStories', '')
        
        table += f"| {feature_id} | {name} | {description} | {target_completion} | {progress}% | {related_stories} |\n"
    
    return table


def generate_planned_features_table(features: List[Dict[str, str]]) -> str:
    """Generate a markdown table for planned features.

    Args:
        features: List of feature dictionaries

    Returns:
        Markdown table as a string
    """
    planned_features = [f for f in features if f.get('Status', '').lower() == 'planned']
    
    if not planned_features:
        return "No planned features yet.\n"
    
    table = "| Feature ID | Feature Name | Description | Target Start | Priority | Related Stories |\n"
    table += "|------------|-------------|-------------|-------------|----------|----------------|\n"
    
    for feature in planned_features:
        feature_id = feature.get('FeatureID', '')
        name = feature.get('Name', '')
        description = feature.get('Description', '')
        target_start = feature.get('TargetStart', '')
        priority = feature.get('Priority', '')
        related_stories = feature.get('RelatedStories', '')
        
        table += f"| {feature_id} | {name} | {description} | {target_start} | {priority} | {related_stories} |\n"
    
    return table


def generate_feature_to_story_mapping(features: List[Dict[str, str]], stories: List[Dict[str, str]]) -> str:
    """Generate feature-to-story mapping section.

    Args:
        features: List of feature dictionaries
        stories: List of story dictionaries

    Returns:
        Markdown content as a string
    """
    if not features:
        return "No features available for mapping.\n"
    
    content = ""
    
    # Create a dictionary to map feature IDs to their stories
    feature_stories = {}
    for story in stories:
        feature_id = story.get('FeatureID', '')
        if feature_id:
            if feature_id not in feature_stories:
                feature_stories[feature_id] = []
            feature_stories[feature_id].append(story)
    
    for feature in features:
        feature_id = feature.get('FeatureID', '')
        name = feature.get('Name', '')
        description = feature.get('Description', '')
        
        content += f"### Feature: {feature_id} - {name}\n\n"
        content += f"**Description**: {description}\n\n"
        content += "**User Stories**:\n"
        
        if feature_id in feature_stories and feature_stories[feature_id]:
            for story in feature_stories[feature_id]:
                story_id = story.get('StoryID', '')
                story_desc = story.get('Description', '')
                content += f"- {story_id} - {story_desc}\n"
        else:
            content += "- No stories linked to this feature yet.\n"
        
        content += "\n"
    
    return content


def generate_metrics_section(features: List[Dict[str, str]], stories: List[Dict[str, str]]) -> str:
    """Generate metrics and progress indicators section.

    Args:
        features: List of feature dictionaries
        stories: List of story dictionaries

    Returns:
        Markdown content as a string
    """
    completed_features = sum(1 for f in features if f.get('Status', '').lower() == 'completed')
    total_features = len(features) if features else 0
    feature_completion = f"{completed_features}/{total_features} ({int(completed_features/total_features*100) if total_features else 0}%)" if total_features else "0/0 (0%)"
    
    completed_stories = sum(1 for s in stories if s.get('Status', '').lower() == 'completed')
    total_stories = len(stories) if stories else 0
    story_completion = f"{completed_stories}/{total_stories} ({int(completed_stories/total_stories*100) if total_stories else 0}%)" if total_stories else "0/0 (0%)"
    
    content = "### Overall Product Completion\n"
    content += f"- Features completed: {feature_completion}\n"
    content += f"- Stories implemented: {story_completion}\n\n"
    
    # Calculate sprint velocity if data is available
    sprint_stories = {}
    sprint_points = {}
    
    for story in stories:
        sprint = story.get('Sprint', '')
        status = story.get('Status', '').lower()
        points = story.get('StoryPoints', '0')
        
        if sprint and status == 'completed':
            if sprint not in sprint_stories:
                sprint_stories[sprint] = 0
                sprint_points[sprint] = 0
            
            sprint_stories[sprint] += 1
            sprint_points[sprint] += int(points) if points.isdigit() else 0
    
    num_sprints = len(sprint_stories)
    avg_stories = sum(sprint_stories.values()) / num_sprints if num_sprints else 0
    avg_points = sum(sprint_points.values()) / num_sprints if num_sprints else 0
    
    content += "### Sprint Velocity\n"
    content += f"- Average stories completed per sprint: {avg_stories:.1f}\n"
    content += f"- Average story points per sprint: {avg_points:.1f}\n"
    
    return content


def update_product_state_document() -> None:
    """Update the product state markdown document with data from CSV files."""
    # Read data from CSV files
    features = read_csv_file(FEATURES_CSV_PATH)
    stories = read_csv_file(STORIES_CSV_PATH)
    
    # Read existing markdown content
    markdown_content = read_markdown_file(PRODUCT_STATE_PATH)
    
    # If the file doesn't exist or is empty, create a new one with headers
    if not markdown_content:
        markdown_content = """# Product State Tracking

## Overview
This document tracks the current state of the product, including completed features, in-progress work, and planned features. It serves as a bridge between the high-level roadmap and the detailed implementation work.

## Current Product State

### Completed Features
REPLACE_COMPLETED_FEATURES

### In-Progress Features
REPLACE_IN_PROGRESS_FEATURES

### Planned Features (Next Up)
REPLACE_PLANNED_FEATURES

## Feature-to-Story Mapping

This section maps features to their constituent user stories, providing traceability between high-level features and implementation details.

REPLACE_FEATURE_STORY_MAPPING

## Metrics and Progress Indicators

REPLACE_METRICS

## Blueprint Alignment

This section tracks how the current product state aligns with the blueprints defined in other documentation.

### Deployment Principles Alignment (ref: 04_feature_blueprints_from_slueth.md)
- Small Incremental Changes: [Status]
- Automated Testing: [Status]
- Continuous Integration: [Status]
- Deployment Automation: [Status]
- Monitoring and Observability: [Status]
- Fast Rollbacks: [Status]

### DevOps Principles Alignment (ref: 05_accelerate_devops_principles.md)
- Deployment Frequency: [Current state]
- Lead Time for Changes: [Current state]
- Mean Time to Recover: [Current state]
- Change Failure Rate: [Current state]

## Gap Analysis

This section identifies gaps between the current product state and the target state defined in the roadmap and vision documents.

### Feature Gaps
[List features that are in the roadmap but not yet implemented or planned]

### Technical Debt
[List known technical debt items that need to be addressed]

## Update History

| Date | Updated By | Changes Made |
|------|------------|-------------|
| CURRENT_DATE | Script | Initial import from CSV |
""".replace('CURRENT_DATE', datetime.now().strftime('%Y-%m-%d'))
    
    # Generate tables and sections
    completed_features_table = generate_completed_features_table(features)
    in_progress_features_table = generate_in_progress_features_table(features)
    planned_features_table = generate_planned_features_table(features)
    feature_story_mapping = generate_feature_to_story_mapping(features, stories)
    metrics_section = generate_metrics_section(features, stories)
    
    # Update the markdown content
    markdown_content = markdown_content.replace('REPLACE_COMPLETED_FEATURES', completed_features_table)
    markdown_content = markdown_content.replace('REPLACE_IN_PROGRESS_FEATURES', in_progress_features_table)
    markdown_content = markdown_content.replace('REPLACE_PLANNED_FEATURES', planned_features_table)
    markdown_content = markdown_content.replace('REPLACE_FEATURE_STORY_MAPPING', feature_story_mapping)
    markdown_content = markdown_content.replace('REPLACE_METRICS', metrics_section)
    
    # Add update history entry
    update_history_pattern = r'(## Update History\s*\n\s*\|\s*Date\s*\|\s*Updated By\s*\|\s*Changes Made\s*\|\s*\n\s*\|[-\s]*\|[-\s]*\|[-\s]*\|\s*\n)'
    update_entry = f"| {datetime.now().strftime('%Y-%m-%d')} | Script | Updated from CSV files |\n"
    
    if re.search(update_history_pattern, markdown_content):
        markdown_content = re.sub(update_history_pattern, f"\g<1>{update_entry}", markdown_content)
    
    # Write updated content back to the file
    write_markdown_file(PRODUCT_STATE_PATH, markdown_content)
    print(f"Product state document updated: {PRODUCT_STATE_PATH}")


def create_sample_csv_files() -> None:
    """Create sample CSV files if they don't exist."""
    # Sample features CSV
    if not os.path.exists(FEATURES_CSV_PATH):
        with open(FEATURES_CSV_PATH, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['FeatureID', 'Name', 'Description', 'Status', 'Priority', 
                         'CompletionDate', 'TargetCompletion', 'TargetStart', 'Progress', 'RelatedStories']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerow({
                'FeatureID': 'F001',
                'Name': 'Document Ingestion',
                'Description': 'Ability to ingest and process documentation files',
                'Status': 'Completed',
                'Priority': 'High',
                'CompletionDate': '2025-06-15',
                'Progress': '100',
                'RelatedStories': 'S001, S002'
            })
            writer.writerow({
                'FeatureID': 'F002',
                'Name': 'Query Interface',
                'Description': 'User interface for querying the product owner agent',
                'Status': 'In Progress',
                'Priority': 'High',
                'TargetCompletion': '2025-07-15',
                'Progress': '60',
                'RelatedStories': 'S003, S004'
            })
            writer.writerow({
                'FeatureID': 'F003',
                'Name': 'Template Generation',
                'Description': 'Ability to generate document templates based on best practices',
                'Status': 'Planned',
                'Priority': 'Medium',
                'TargetStart': '2025-07-20',
                'RelatedStories': 'S005, S006'
            })
        print(f"Created sample features CSV: {FEATURES_CSV_PATH}")
    
    # Sample stories CSV
    if not os.path.exists(STORIES_CSV_PATH):
        with open(STORIES_CSV_PATH, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['StoryID', 'FeatureID', 'Description', 'Status', 'StoryPoints', 'Sprint', 'Assignee']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerow({
                'StoryID': 'S001',
                'FeatureID': 'F001',
                'Description': 'As a user, I want to upload markdown files so they can be processed by the agent',
                'Status': 'Completed',
                'StoryPoints': '5',
                'Sprint': 'Sprint 1',
                'Assignee': 'Alex'
            })
            writer.writerow({
                'StoryID': 'S002',
                'FeatureID': 'F001',
                'Description': 'As a user, I want the system to extract key information from uploaded documents',
                'Status': 'Completed',
                'StoryPoints': '8',
                'Sprint': 'Sprint 1',
                'Assignee': 'Sam'
            })
            writer.writerow({
                'StoryID': 'S003',
                'FeatureID': 'F002',
                'Description': 'As a user, I want a command-line interface to query the agent',
                'Status': 'Completed',
                'StoryPoints': '3',
                'Sprint': 'Sprint 2',
                'Assignee': 'Jordan'
            })
            writer.writerow({
                'StoryID': 'S004',
                'FeatureID': 'F002',
                'Description': 'As a user, I want to receive relevant answers based on the documentation',
                'Status': 'In Progress',
                'StoryPoints': '5',
                'Sprint': 'Sprint 2',
                'Assignee': 'Taylor'
            })
            writer.writerow({
                'StoryID': 'S005',
                'FeatureID': 'F003',
                'Description': 'As a product owner, I want to generate user story templates',
                'Status': 'Planned',
                'StoryPoints': '3',
                'Sprint': 'Sprint 3',
                'Assignee': 'Unassigned'
            })
            writer.writerow({
                'StoryID': 'S006',
                'FeatureID': 'F003',
                'Description': 'As a product owner, I want to generate sprint planning templates',
                'Status': 'Planned',
                'StoryPoints': '2',
                'Sprint': 'Sprint 3',
                'Assignee': 'Unassigned'
            })
        print(f"Created sample stories CSV: {STORIES_CSV_PATH}")


def main() -> None:
    """Main function to run the script."""
    print("Product State Import Script")
    print("==========================")
    
    # Create sample CSV files if they don't exist
    create_sample_csv_files()
    
    # Update the product state document
    update_product_state_document()
    
    print("\nDone!")


if __name__ == "__main__":
    main()
