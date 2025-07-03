# Templates for Common Product Artifacts

This document provides standardized templates for common product management artifacts. These templates can be used by the product owner agent to assist in document creation and ensure consistency across the product development lifecycle.

## Table of Contents

1. [User Story Template](#user-story-template)
2. [Feature Specification Template](#feature-specification-template)
3. [Product Requirements Document (PRD)](#product-requirements-document)
4. [Sprint Planning Template](#sprint-planning-template)
5. [Retrospective Template](#retrospective-template)
6. [Product Roadmap Template](#product-roadmap-template)
7. [Release Plan Template](#release-plan-template)
8. [Stakeholder Communication Template](#stakeholder-communication-template)
9. [User Research Plan Template](#user-research-plan-template)
10. [Feature Rollout Plan Template](#feature-rollout-plan-template)

---

## User Story Template

```markdown
# User Story: [Story ID]

## Title
[Concise description of the story]

## User Story
As a [type of user],
I want [goal/objective],
So that [benefit/value].

## Acceptance Criteria
1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]

## Additional Details
- **Priority**: [Must Have / Should Have / Could Have / Won't Have]
- **Story Points**: [Fibonacci number: 1, 2, 3, 5, 8, 13, etc.]
- **Dependencies**: [List any dependencies]
- **Related Stories**: [List related story IDs]

## Technical Notes
[Any technical considerations or implementation details]

## Mockups/Screenshots
[Links or embedded images if applicable]

## Testing Notes
[Specific testing requirements or scenarios]
```

---

## Feature Specification Template

```markdown
# Feature Specification: [Feature Name]

## Overview
[Brief description of the feature and its purpose]

## Business Case
[Explain why this feature is important, including business goals and user needs it addresses]

## Success Metrics
[Define how success will be measured for this feature]
- Metric 1: [description and target]
- Metric 2: [description and target]

## User Stories
[List of user stories that comprise this feature]
1. [User Story ID and title]
2. [User Story ID and title]

## Functional Requirements
[Detailed description of what the feature should do]

### Must Have
- [Requirement 1]
- [Requirement 2]

### Should Have
- [Requirement 3]
- [Requirement 4]

### Could Have
- [Requirement 5]
- [Requirement 6]

## Non-Functional Requirements
- **Performance**: [Requirements]
- **Security**: [Requirements]
- **Accessibility**: [Requirements]
- **Scalability**: [Requirements]

## User Experience
[Description of the user flow and experience]

### Mockups
[Links to design mockups or embedded images]

## Technical Implementation
[High-level technical approach]

### System Components
[Components that will be affected]

### Data Model Changes
[Any changes to the data model]

### API Changes
[Any changes to APIs]

## Testing Strategy
[Approach to testing this feature]

## Rollout Plan
[Strategy for releasing this feature]

## Open Questions
[List any unresolved questions or decisions]
```

---

## Product Requirements Document

```markdown
# Product Requirements Document: [Product/Feature Name]

## Document History
| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 0.1 | [Date] | [Name] | Initial draft |

## Executive Summary
[Brief overview of the product/feature and its strategic importance]

## Problem Statement
[Clear description of the problem being solved]

## Target Users
[Description of the target user segments]

## User Personas
[Detailed user personas if applicable]

## Goals and Objectives
[Specific, measurable goals for the product/feature]

## Success Metrics
[How success will be measured]

## Product/Feature Requirements

### Functional Requirements
[Detailed list of functional requirements]

### Non-Functional Requirements
[Performance, security, scalability, etc.]

## User Flows
[Description of key user journeys]

## Design Specifications
[Links to design documents or embedded mockups]

## Technical Considerations
[Technical constraints, dependencies, or implementation notes]

## Go-to-Market Strategy
[How the product/feature will be launched and marketed]

## Timeline
[High-level timeline for development and release]

## Risks and Mitigations
[Identified risks and mitigation strategies]

## Appendix
[Additional supporting information]
```

---

## Sprint Planning Template

```markdown
# Sprint Planning: Sprint [Number]

## Sprint Details
- **Sprint Duration**: [Start Date] to [End Date]
- **Team Capacity**: [Available person-days]
- **Sprint Goal**: [Concise statement of sprint objective]

## Sprint Backlog

### Committed User Stories
| ID | Title | Story Points | Assignee | Notes |
|----|-------|--------------|----------|-------|
| [ID] | [Title] | [Points] | [Name] | [Notes] |

### Technical Debt Items
| ID | Title | Story Points | Assignee | Notes |
|----|-------|--------------|----------|-------|
| [ID] | [Title] | [Points] | [Name] | [Notes] |

### Bug Fixes
| ID | Title | Priority | Assignee | Notes |
|----|-------|----------|----------|-------|
| [ID] | [Title] | [Priority] | [Name] | [Notes] |

## Dependencies
[List any external dependencies that might impact the sprint]

## Risks and Concerns
[Identify potential risks for this sprint]

## Definition of Done
[Criteria that must be met for work to be considered complete]

## Sprint Demo Plan
[Plan for demonstrating completed work]
```

---

## Retrospective Template

```markdown
# Sprint Retrospective: Sprint [Number]

## Sprint Summary
- **Sprint Duration**: [Start Date] to [End Date]
- **Sprint Goal**: [Sprint goal]
- **Completed Story Points**: [X] out of [Y] committed ([Z]%)
- **Velocity**: [Story points completed]

## What Went Well
- [Item 1]
- [Item 2]
- [Item 3]

## What Could Be Improved
- [Item 1]
- [Item 2]
- [Item 3]

## Action Items
| Action | Owner | Due Date |
|--------|-------|----------|
| [Action] | [Name] | [Date] |

## Team Mood
[Brief description of team sentiment]

## Key Learnings
[Important insights gained during this sprint]

## Looking Ahead
[Considerations for the next sprint]
```

---

## Product Roadmap Template

```markdown
# Product Roadmap: [Product Name]

## Vision
[Product vision statement]

## Strategic Goals
[Key strategic goals the roadmap supports]

## Roadmap Overview

### Now (Current Quarter)
- **Theme**: [Theme name]
- **Key Deliverables**:
  - [Deliverable 1]
  - [Deliverable 2]
- **Expected Outcomes**:
  - [Outcome 1]
  - [Outcome 2]

### Next (Next Quarter)
- **Theme**: [Theme name]
- **Key Deliverables**:
  - [Deliverable 1]
  - [Deliverable 2]
- **Expected Outcomes**:
  - [Outcome 1]
  - [Outcome 2]

### Later (2+ Quarters Out)
- **Theme**: [Theme name]
- **Key Deliverables**:
  - [Deliverable 1]
  - [Deliverable 2]
- **Expected Outcomes**:
  - [Outcome 1]
  - [Outcome 2]

## Key Milestones
| Milestone | Target Date | Status |
|-----------|-------------|--------|
| [Milestone] | [Date] | [Status] |

## Dependencies and Risks
[Key dependencies and risks that may impact the roadmap]

## Assumptions
[Key assumptions made in creating this roadmap]

## Revision History
| Version | Date | Changes |
|---------|------|--------|
| [Version] | [Date] | [Changes] |
```

---

## Release Plan Template

```markdown
# Release Plan: [Release Name/Version]

## Release Overview
- **Version**: [Version number]
- **Release Date**: [Target date]
- **Release Manager**: [Name]

## Release Goals
[Primary objectives for this release]

## Feature Set
| Feature | Description | Status | Owner |
|---------|-------------|--------|-------|
| [Feature] | [Description] | [Status] | [Name] |

## Release Timeline
| Milestone | Date | Deliverables |
|-----------|------|-------------|
| Feature Freeze | [Date] | [Deliverables] |
| Code Freeze | [Date] | [Deliverables] |
| QA Complete | [Date] | [Deliverables] |
| Release Candidate | [Date] | [Deliverables] |
| Production Release | [Date] | [Deliverables] |

## Testing Strategy
[Approach to testing for this release]

## Deployment Plan
[Steps for deploying this release]

## Rollback Plan
[Process for rolling back if necessary]

## Communication Plan
| Audience | Message | Channel | Timing | Owner |
|----------|---------|---------|--------|-------|
| [Audience] | [Message] | [Channel] | [Timing] | [Name] |

## Success Criteria
[Metrics to determine release success]

## Post-Release Monitoring
[Plan for monitoring after release]
```

---

## Stakeholder Communication Template

```markdown
# Stakeholder Update: [Project/Product Name]

## Date
[Date of communication]

## Executive Summary
[Brief overview of current status and key points]

## Progress Update

### Accomplishments
[Key accomplishments since last update]

### Current Status
[Overall status: On Track / At Risk / Off Track]

### Key Metrics
[Important metrics and their current values]

## Timeline
[Updated timeline with any changes highlighted]

## Risks and Issues

| Risk/Issue | Impact | Mitigation/Resolution | Owner |
|------------|--------|------------------------|-------|
| [Risk/Issue] | [Impact] | [Mitigation/Resolution] | [Name] |

## Decisions Needed
[List any decisions required from stakeholders]

## Next Steps
[Upcoming work and milestones]

## Questions and Discussion Points
[Topics for discussion]
```

---

## User Research Plan Template

```markdown
# User Research Plan: [Research Initiative]

## Research Goals
[Clear statement of what you want to learn]

## Research Questions
[Specific questions the research should answer]

## Methodology
[Research methods to be used]

## Participant Profile
[Description of target participants]

## Recruitment Plan
[How participants will be recruited]

## Research Script/Protocol
[Outline of the research process]

## Timeline
| Activity | Date |
|----------|------|
| [Activity] | [Date] |

## Resources Needed
[Tools, people, and other resources required]

## Analysis Plan
[How data will be analyzed]

## Deliverables
[Expected outputs from the research]

## Stakeholders
[Who needs to be informed or involved]
```

---

## Feature Rollout Plan Template

```markdown
# Feature Rollout Plan: [Feature Name]

## Feature Overview
[Brief description of the feature]

## Rollout Strategy
[Approach to rolling out the feature: phased, all at once, etc.]

## Rollout Phases

### Phase 1: [Name]
- **Target Audience**: [Description]
- **Percentage of Users**: [%]
- **Start Date**: [Date]
- **Success Criteria**: [Criteria]
- **Monitoring Plan**: [Plan]

### Phase 2: [Name]
- **Target Audience**: [Description]
- **Percentage of Users**: [%]
- **Start Date**: [Date]
- **Success Criteria**: [Criteria]
- **Monitoring Plan**: [Plan]

## Feature Flag Strategy
[How feature flags will be used]

## Metrics to Monitor
[Key metrics to track during rollout]

## Rollback Criteria and Plan
[When and how to roll back if necessary]

## Communication Plan
| Audience | Message | Channel | Timing |
|----------|---------|---------|--------|
| [Audience] | [Message] | [Channel] | [Timing] |

## Support Plan
[How support issues will be handled]
```

## Cross-Reference with Other Documents

- For alignment with product vision, see [00_vision_and_strategy.md](./00_vision_and_strategy.md)
- For roadmap planning, see [01_roadmap.md](./01_roadmap.md)
- For team allocation, see [02_teams_and_allocation.md](./02_teams_and_allocation.md)
- For technical considerations, see [03_architecture_and_principles.md](./03_architecture_and_principles.md)
- For deployment practices, see [04_feature_blueprints_from_slueth.md](./04_feature_blueprints_from_slueth.md)
- For DevOps principles, see [05_accelerate_devops_principles.md](./05_accelerate_devops_principles.md)
- For terminology reference, see [06_glossary_of_terms.md](./06_glossary_of_terms.md)
- For decision-making guidance, see [07_decision_frameworks.md](./07_decision_frameworks.md)
