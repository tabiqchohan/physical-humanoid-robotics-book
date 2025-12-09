# Data Model: Physical AI & Humanoid Robotics Book

## Entity Definitions

### Chapter
- **Description**: A major section of the book covering a specific topic
- **Attributes**:
  - id: string (e.g., "ch01", "ch02")
  - title: string (chapter title)
  - number: integer (chapter sequence number)
  - wordCount: range (min and max word count)
  - prerequisiteKnowledge: string (required background knowledge)
  - learningOutcomes: array of strings (specific learning objectives)
  - subtopics: array of strings (detailed subtopics)
  - status: enum (draft, reviewed, validated, published)
  - author: string (assigned author)
  - reviewer: string (assigned technical reviewer)

### Subtopic
- **Description**: A specific area of focus within a chapter
- **Attributes**:
  - id: string (e.g., "ch01-s01")
  - chapterId: string (reference to parent chapter)
  - title: string (subtopic title)
  - description: string (brief explanation)
  - technicalDepth: enum (introductory, intermediate, advanced)
  - relatedConcepts: array of strings (linked concepts)

### LearningOutcome
- **Description**: A measurable result that readers should achieve after completing a chapter
- **Attributes**:
  - id: string (e.g., "lo01-01")
  - chapterId: string (reference to parent chapter)
  - description: string (what the reader will be able to do)
  - assessmentMethod: string (how the outcome will be validated)
  - difficultyLevel: enum (basic, intermediate, advanced)

### CodeExample
- **Description**: A practical implementation demonstrating concepts from the book
- **Attributes**:
  - id: string (e.g., "ce01-01")
  - chapterId: string (reference to parent chapter)
  - title: string (brief description)
  - language: string (programming language)
  - description: string (what the example demonstrates)
  - prerequisites: array of strings (requirements to run the example)
  - sourceCode: string (path to source file)
  - dependencies: array of strings (required libraries/packages)
  - validationStatus: enum (untested, tested, validated)
  - complexity: enum (simple, moderate, complex)

### VisualAsset
- **Description**: Diagram, chart, photo, or 3D render used to illustrate concepts
- **Attributes**:
  - id: string (e.g., "va01-01")
  - chapterId: string (reference to parent chapter)
  - type: enum (diagram, chart, photo, 3d-render, animation)
  - title: string (brief description)
  - description: string (what the asset illustrates)
  - fileLocation: string (path to asset file)
  - resolution: string (dimensions for print/digital)
  - accessibilityAltText: string (text description for accessibility)
  - technicalAccuracy: boolean (verified for technical correctness)
  - usageRights: string (license/copyright information)

### TechnicalReview
- **Description**: Review process for validating technical accuracy of content
- **Attributes**:
  - id: string (e.g., "tr01")
  - targetId: string (chapter, code example, or visual asset ID)
  - targetType: enum (chapter, code-example, visual-asset)
  - reviewer: string (expert reviewer name)
  - reviewDate: date (when review was completed)
  - status: enum (pending, in-progress, completed, rejected)
  - findings: array of strings (issues found during review)
  - recommendations: array of strings (suggested improvements)
  - approval: boolean (whether content passes technical validation)

## Entity Relationships

### Chapter → Subtopic
- **Relationship**: One-to-Many
- **Description**: Each chapter contains 3-5 subtopics
- **Cardinality**: 1 chapter : 3-5 subtopics

### Chapter → LearningOutcome
- **Relationship**: One-to-Many
- **Description**: Each chapter defines 3 measurable learning outcomes
- **Cardinality**: 1 chapter : 3 learning outcomes

### Chapter → CodeExample
- **Relationship**: One-to-Many
- **Description**: Each chapter may include multiple code examples
- **Cardinality**: 1 chapter : 0-N code examples

### Chapter → VisualAsset
- **Relationship**: One-to-Many
- **Description**: Each chapter may include multiple visual assets
- **Cardinality**: 1 chapter : 0-N visual assets

### Chapter → TechnicalReview
- **Relationship**: One-to-Many
- **Description**: Each chapter may undergo multiple technical reviews
- **Cardinality**: 1 chapter : 0-N technical reviews

## Validation Rules

### Chapter Validation
- **Title**: Must be 10-100 characters
- **Word Count**: Must be within specified range (500-2000 words)
- **Subtopics**: Must have 3-5 subtopics defined
- **Learning Outcomes**: Must have exactly 3 measurable outcomes
- **Prerequisite Knowledge**: Must be specified

### CodeExample Validation
- **Language**: Must be one of supported languages (Python, C++, MATLAB, etc.)
- **Source Code**: Must exist at specified file location
- **Dependencies**: Must be documented and resolvable
- **Validation Status**: Must be validated before publication

### VisualAsset Validation
- **File Location**: Must exist and be accessible
- **Technical Accuracy**: Must be verified by technical expert
- **Resolution**: Must meet minimum requirements for intended use
- **Accessibility**: Must include alt text for accessibility

## State Transitions

### Chapter States
- **Draft** → **Reviewed** (after peer review)
- **Reviewed** → **Validated** (after technical validation)
- **Validated** → **Published** (after final QA)
- **Published** → **Archived** (after publication)

### CodeExample States
- **Created** → **Implemented** (code written)
- **Implemented** → **Tested** (code executed successfully)
- **Tested** → **Validated** (reviewed by expert)
- **Validated** → **Published** (included in book)

### VisualAsset States
- **Concept** → **Created** (asset produced)
- **Created** → **Reviewed** (accuracy verified)
- **Reviewed** → **Optimized** (size/format optimized)
- **Optimized** → **Published** (included in book)

## Indexes

### Primary Indexes
- Chapter.id (unique)
- Subtopic.id (unique)
- LearningOutcome.id (unique)
- CodeExample.id (unique)
- VisualAsset.id (unique)
- TechnicalReview.id (unique)

### Secondary Indexes
- Chapter.number (for sequential access)
- Chapter.status (for workflow management)
- CodeExample.chapterId (for chapter-based queries)
- VisualAsset.chapterId (for chapter-based queries)
- TechnicalReview.targetId (for review lookup)