# Code Examples Contract: Physical AI & Humanoid Robotics Book

## Overview

This contract defines the interface, structure, and validation requirements for all code examples in the Physical AI & Humanoid Robotics book. It ensures consistency, reliability, and educational value across all examples.

## Code Example Interface Specification

### Required Structure
Each code example must conform to the following structure:

```
code-examples/chapter-XX-example-name/
├── README.md                 # Example description and usage
├── main.py                   # Main executable code
├── requirements.txt          # Python dependencies (if applicable)
├── config.yaml               # Configuration parameters
├── test_example.py           # Test/validation script
├── expected_output.txt       # Expected results
└── assets/                   # Supporting files
    ├── input_data/
    └── output_visuals/
```

### Mandatory Files

#### README.md
```markdown
# [Example Name]

## Description
Brief explanation of what the example demonstrates.

## Prerequisites
- Python 3.8+
- Required packages (list)
- System requirements

## Usage
```bash
python main.py --parameter value
```

## Expected Output
Description of what the example should produce.

## Learning Objectives
- Objective 1
- Objective 2
- Objective 3
```

#### main.py
Must include:
- Clear module-level documentation
- Type hints for all functions
- Error handling
- Configurable parameters
- Main execution block with `if __name__ == "__main__":`

### Configuration Contract

#### config.yaml
```yaml
# Example metadata
example_id: "ch03-kinematics-calculator"
title: "Forward Kinematics Calculator"
description: "Calculate end-effector position from joint angles"
author: "Book Author"
version: "1.0.0"

# Execution parameters
parameters:
  joint_angles:
    type: "list[float]"
    default: [0.0, 0.0, 0.0]
    description: "Joint angles in radians"
  link_lengths:
    type: "list[float]"
    default: [1.0, 1.0, 0.5]
    description: "Link lengths in meters"

# Validation settings
validation:
  timeout_seconds: 30
  expected_runtime: "fast"  # fast, medium, slow
  resource_limits:
    memory_mb: 512
    cpu_percent: 80
```

## Input/Output Contracts

### Standard Input Interface
All examples must accept configuration via:
1. Command-line arguments using argparse
2. Configuration file (config.yaml)
3. Environment variables as fallback

### Standard Output Interface
All examples must provide output in:
1. Console output with clear formatting
2. Optional file output (if applicable)
3. Return codes (0 for success, non-zero for errors)

### Example Input Contract
```python
import argparse
import yaml

def parse_arguments():
    parser = argparse.ArgumentParser(description='Example description')
    parser.add_argument('--config', type=str, default='config.yaml',
                       help='Path to configuration file')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose output')
    return parser.parse_args()

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)
```

### Example Output Contract
```python
def print_results(results, verbose=False):
    if verbose:
        print("Detailed Results:")
        for key, value in results.items():
            print(f"  {key}: {value}")
    else:
        print(f"Result: {results['main_output']}")

    return results
```

## Validation Requirements

### Functional Validation
Each code example must:
- Execute without errors for valid inputs
- Handle invalid inputs gracefully
- Complete within specified time limits
- Produce consistent output for same inputs

### Educational Validation
Each code example must:
- Demonstrate a specific concept from the book
- Include appropriate comments and documentation
- Follow best practices for the programming language
- Be pedagogically appropriate for the target audience

### Technical Validation
Each code example must:
- Pass linting checks (flake8, mypy, etc.)
- Include unit tests where appropriate
- Handle edge cases appropriately
- Use appropriate error handling

## Quality Standards

### Code Quality
- Follow PEP 8 style guidelines for Python
- Include type hints for function parameters and return values
- Use meaningful variable and function names
- Limit function length to 50 lines maximum

### Documentation Quality
- Include module-level docstrings
- Document all public functions
- Include example usage in docstrings
- Explain the purpose of each parameter

### Performance Requirements
- Execute within 30 seconds for typical inputs (unless otherwise specified)
- Use memory efficiently
- Include progress indicators for long-running operations

## Error Handling Contract

### Error Types
All examples must handle:
- Input validation errors
- Resource availability errors
- External dependency errors
- Computational errors (e.g., singularities in kinematics)

### Error Reporting
```python
class ExampleError(Exception):
    """Base exception for book examples"""
    pass

class InputValidationError(ExampleError):
    """Raised when input parameters are invalid"""
    pass

def validate_inputs(inputs):
    if not isinstance(inputs, dict):
        raise InputValidationError("Inputs must be a dictionary")
    # Additional validation logic
```

## Testing Contract

### Test Structure
Each example must include a test file with:
- Unit tests for core functions
- Integration tests for full execution
- Edge case tests
- Performance tests (where applicable)

### Test Requirements
```python
import unittest
import time
from main import calculate_forward_kinematics

class TestForwardKinematics(unittest.TestCase):
    def test_basic_calculation(self):
        """Test basic forward kinematics calculation"""
        result = calculate_forward_kinematics([0, 0, 0], [1, 1, 1])
        expected = [2, 0, 1]  # Expected end-effector position
        self.assertAlmostEqual(result[0], expected[0], places=2)
        self.assertAlmostEqual(result[1], expected[1], places=2)
        self.assertAlmostEqual(result[2], expected[2], places=2)

    def test_performance(self):
        """Test that calculation completes within time limit"""
        start_time = time.time()
        calculate_forward_kinematics([0.1, 0.2, 0.3], [1, 1, 1])
        execution_time = time.time() - start_time
        self.assertLess(execution_time, 1.0)  # Should complete in < 1 second
```

## Versioning and Compatibility

### Language Versions
- Python examples: Compatible with Python 3.8+
- Dependencies: Specify minimum versions in requirements.txt
- ROS examples: Compatible with ROS Noetic and ROS 2

### Backward Compatibility
- Maintain compatibility with specified dependency versions
- Provide migration path for breaking changes
- Include version checks where appropriate

## Security Considerations

### Input Sanitization
- Validate all external inputs
- Prevent code injection through configuration files
- Use safe YAML loading (yaml.safe_load)

### Resource Management
- Limit memory and CPU usage
- Properly close file handles and connections
- Include timeout mechanisms for external calls

## Compliance with Book Principles

### Safety-First Design
- Include safety checks in simulation code
- Provide warnings for potentially unsafe operations
- Include emergency stop mechanisms where applicable

### Ethical Considerations
- Include appropriate disclaimers about limitations
- Avoid biased algorithms or datasets
- Include fairness and transparency considerations

### Transparency
- Include source code for all algorithms
- Document assumptions and limitations
- Provide clear explanations of methods used