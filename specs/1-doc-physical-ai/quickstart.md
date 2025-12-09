# Quickstart Guide: Physical AI & Humanoid Robotics Book

## Getting Started

This guide will help you set up your environment to work with the Physical AI & Humanoid Robotics book content, including code examples, simulations, and development tools.

## Prerequisites

Before starting, ensure you have the following installed:

### System Requirements
- Operating System: Ubuntu 20.04+ or macOS 10.15+
- RAM: 8GB minimum (16GB recommended)
- Storage: 10GB available space
- Python: 3.8 or higher

### Required Software
1. **Git** for version control
   ```bash
   # Ubuntu
   sudo apt update && sudo apt install git

   # macOS
   xcode-select --install
   ```

2. **Python 3.8+** with pip
   ```bash
   # Check version
   python3 --version

   # Install if needed (Ubuntu)
   sudo apt install python3 python3-pip
   ```

3. **LaTeX** for mathematical notation rendering
   ```bash
   # Ubuntu
   sudo apt install texlive-full

   # macOS
   # Download MacTeX from https://www.tug.org/mactex/
   ```

## Repository Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd physical-ai-book
   ```

2. **Set up virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Working with Code Examples

### Python Examples
1. **Navigate to a chapter's code directory**
   ```bash
   cd code-examples/chapter-03
   ```

2. **Install chapter-specific dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run an example**
   ```bash
   python3 kinematics_calculator.py
   ```

### ROS Integration
1. **Set up ROS environment**
   ```bash
   source /opt/ros/noetic/setup.bash
   source devel/setup.bash
   ```

2. **Run ROS examples**
   ```bash
   roslaunch physical_ai_examples example.launch
   ```

## Simulation Environment

### Setting up Gazebo
1. **Install Gazebo**
   ```bash
   # Ubuntu
   sudo apt install gazebo11 libgazebo11-dev
   ```

2. **Run a simulation example**
   ```bash
   roslaunch gazebo_ros empty_world.launch
   ```

### Setting up PyBullet
1. **Install PyBullet**
   ```bash
   pip install pybullet
   ```

2. **Run a physics simulation**
   ```bash
   python3 examples/bullet_simulation.py
   ```

## Development Workflow

### Creating New Content
1. **Create a feature branch**
   ```bash
   git checkout -b feat/new-chapter-content
   ```

2. **Add your content to the appropriate directory**
   ```bash
   # For chapter content
   mkdir -p chapters/XX-chapter-title
   # Add your markdown files
   ```

3. **Validate your content**
   ```bash
   # Run validation scripts
   python3 scripts/validate_content.py chapters/XX-chapter-title/
   ```

### Running Tests
1. **Run code example tests**
   ```bash
   python3 -m pytest tests/code_examples/
   ```

2. **Validate mathematical formulas**
   ```bash
   python3 scripts/validate_math.py
   ```

3. **Check visual asset references**
   ```bash
   python3 scripts/check_assets.py
   ```

## Building the Book

### PDF Generation
```bash
# Install pandoc if not already installed
sudo apt install pandoc texlive-xetex

# Generate PDF
make pdf
# or
bash scripts/build_pdf.sh
```

### HTML Generation
```bash
# Generate HTML
make html
# or
bash scripts/build_html.sh
```

### ePub Generation
```bash
# Generate ePub
make epub
# or
bash scripts/build_epub.sh
```

## Quality Assurance

### Code Validation
```bash
# Run all code examples to ensure they work
python3 scripts/test_all_examples.py

# Check code style
flake8 code-examples/
```

### Content Validation
```bash
# Validate all cross-references
python3 scripts/validate_crossrefs.py

# Check for broken links
python3 scripts/check_links.py
```

## Contributing

### Branch Naming Convention
- Feature branches: `feat/chapter-XX-topic`
- Bug fixes: `fix/chapter-XX-issue`
- Documentation: `docs/chapter-XX-update`

### Commit Message Format
```
feat: Add new section on humanoid kinematics

- Implement forward kinematics example
- Add inverse kinematics explanation
- Include mathematical derivations
```

### Pull Request Process
1. Ensure all tests pass
2. Update documentation if needed
3. Get technical review
4. Submit PR with clear description

## Troubleshooting

### Common Issues

**Problem**: Code examples don't run
**Solution**: Check that all dependencies are installed and virtual environment is activated

**Problem**: Mathematical formulas don't render
**Solution**: Ensure LaTeX is properly installed and configured

**Problem**: Simulation environment fails
**Solution**: Verify Gazebo/PyBullet installation and ROS setup

### Getting Help
- Check the issues section for known problems
- Create a new issue if you encounter a problem not listed
- Contact the maintainers through the provided channels

## Next Steps

1. Start with Chapter 1 content in `chapters/01-introduction/`
2. Explore the code examples in `code-examples/`
3. Try running simulations in `simulations/`
4. Review the contribution guidelines in `CONTRIBUTING.md`