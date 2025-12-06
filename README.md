# Physical AI & Humanoid Robotics Documentation

This repository contains the complete documentation for the "Physical AI & Humanoid Robotics" book, published as a Docusaurus site. The documentation covers all aspects of physical artificial intelligence and humanoid robotics development.

## Installation

1. **Prerequisites**
   - Node.js (version 16 or higher)
   - npm or yarn package manager
   - Git

2. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd physical-ai-docs
   npm install
   ```

3. **Install additional dependencies for mathematical content**
   ```bash
   npm install mathjax
   ```

## Local Development

```bash
# Start the development server
npm start

# Build the static site
npm run build

# Serve the built site locally for testing
npm run serve

# Run tests
npm test
```

## Recommended Docusaurus Plugins

This documentation site uses several plugins to enhance functionality:

### Search Plugin
- `@docusaurus/plugin-content-docs` - Built-in search functionality
- Provides full-text search across all documentation pages

### Math Support
- `remark-math` and `rehype-katex` - For rendering mathematical equations
- Enables LaTeX-style math expressions in markdown

### Diagram Support
- `mdx-mermaid` - For creating diagrams and flowcharts
- Integrates Mermaid diagrams directly in documentation

### Image Zoom
- `@docusaurus/plugin-client-redirects` - For enhanced image viewing
- `zoom.js` integration for image zooming capabilities

### Code Block Enhancements
- `@docusaurus/theme-classic` - Enhanced code block features
- Syntax highlighting for multiple programming languages

## Build Commands

```bash
# Build the documentation site
npm run build

# Clean the build cache
npm run clear

# Build with specific environment
NODE_ENV=production npm run build

# Generate static HTML for deployment
npm run build && npm run serve
```

## Deployment (Vercel)

### Prerequisites
- A Vercel account
- Git repository connected to Vercel

### Deployment Steps

1. **Connect your repository to Vercel**
   - Go to https://vercel.com/
   - Import your Git repository
   - Vercel will automatically detect this is a Docusaurus project

2. **Build settings**
   - Build Command: `npm run build`
   - Output Directory: `build`
   - Development Command: `npm start`

3. **Environment variables (if needed)**
   - NODE_VERSION = 18.x (or latest LTS)

4. **Automatic deployment**
   - Push changes to your Git repository
   - Vercel will automatically build and deploy the new version

### Manual deployment with Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy to staging
vercel --env NODE_ENV=production

# Deploy to production
vercel --prod
```

## Project Structure

```
physical-ai-docs/
├── docs/                 # Documentation source files
│   ├── introduction/     # Introduction chapter
│   ├── fundamentals/     # Fundamentals chapter
│   ├── kinematics/       # Kinematics chapter
│   ├── perception/       # Perception chapter
│   ├── control/          # Control theory chapter
│   ├── machine-learning/ # ML for Physical AI chapter
│   ├── planning/         # Planning and navigation chapter
│   ├── hri/              # Human-robot interaction chapter
│   ├── simulation/       # Simulation chapter
│   ├── hardware/         # Hardware design chapter
│   ├── cognitive-architectures/ # Cognitive architectures chapter
│   ├── ethics/           # Ethics and safety chapter
│   ├── healthcare/       # Healthcare applications chapter
│   ├── industrial/       # Industrial applications chapter
│   ├── research-frontiers/ # Research frontiers chapter
│   ├── multi-robot/      # Multi-robot systems chapter
│   ├── learning-demonstrations/ # Learning from demonstrations chapter
│   └── future-directions/ # Future directions chapter
├── src/                  # Custom React components
├── static/               # Static assets (images, etc.)
├── assets/               # Book-specific assets
├── sidebars.js           # Navigation sidebar configuration
├── docusaurus.config.js  # Site configuration
├── package.json          # Dependencies and scripts
└── README.md             # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add and commit your changes (`git add . && git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This documentation is licensed under [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/).
