# Physical AI & Humanoid Robotics Book

This repository hosts the documentation for the book "Physical AI & Humanoid Robotics", built using Docusaurus.

## Installation

To run this project locally, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/physical-ai-robotics.git
    cd physical-ai-robotics
    ```

2.  **Install dependencies:**

    ```bash
    npm install
    # or yarn install
    ```

## Build Commands

-   **Start development server:**

    ```bash
    npm start
    # or yarn start
    ```

    This command starts a local development server and opens a browser window. Most changes are reflected live without restarting the server.

-   **Build static content:**

    ```bash
    npm run build
    # or yarn build
    ```

    This command generates static content into the `build` directory and can be served using any static content hosting service.

## Recommended Plugins

To enhance the Docusaurus site, the following plugins are recommended and can be added to your `docusaurus.config.js`:

-   **@docusaurus/plugin-content-docs (built-in)**: For managing documentation.
-   **@docusaurus/plugin-content-blog (built-in)**: For a blog section.
-   **@docusaurus/plugin-content-pages (built-in)**: For standalone pages.
-   **@docusaurus/plugin-ideal-image**: For optimizing images.
-   **docusaurus-plugin-image-zoom**: For image zoom functionality.
-   **@docusaurus/remark-plugin-math**: For rendering mathematical equations (with `rehype-katex`).
-   **docusaurus-theme-search-algolia / @docusaurus/theme-search-algolia**: For powerful search capabilities.
-   **docusaurus-remark-plugin-mermaid**: For Mermaid diagrams.

## Deployment (Vercel)

To deploy your Docusaurus site to Vercel:

1.  **Install Vercel CLI (if not already installed):**

    ```bash
    npm install -g vercel
    ```

2.  **Deploy your project:**

    ```bash
    vercel
    ```

    Follow the prompts to link your project and deploy. Vercel automatically detects Docusaurus projects and configures the build settings.

    For continuous deployment, integrate your GitHub repository with Vercel.