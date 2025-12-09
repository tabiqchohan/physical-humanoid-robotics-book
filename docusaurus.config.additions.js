// Example additions to docusaurus.config.js for Physical AI & Humanoid Robotics book

// Add to the plugins array:
plugins: [
  // Math support for equations
  [
    '@docusaurus/plugin-content-docs',
    {
      id: 'physical-ai-docs',
      path: 'docs',
      routeBasePath: 'docs',
      sidebarPath: require.resolve('./sidebars.js'),
      editUrl: 'https://github.com/your-org/physical-ai-docs/edit/main/',
      remarkPlugins: [
        require('remark-math'),
        require('mdx-mermaid')
      ],
      rehypePlugins: [
        require('rehype-katex')
      ],
    },
  ],
  // Client redirects for better UX
  [
    '@docusaurus/plugin-client-redirects',
    {
      redirects: [
        {
          to: '/docs/introduction/physical-ai-embodied-intelligence',
          from: ['/docs', '/docs/intro'],
        },
      ],
    },
  ],
],

// Add to the themes array:
themes: [
  // Search functionality
  [
    require.resolve("@easyops-cn/docusaurus-search-local"),
    {
      // Whether to index docs pages
      indexDocs: true,
      // Whether to index blog pages
      indexBlog: false,
      // Whether to index static pages
      indexPages: false,
      // Language used for segmenting words
      language: ["en"],
      // Setting for input placeholder
      placeholder: "Search Physical AI & Humanoid Robotics docs...",
      // Maximum number of search results to be shown
      maxSearchResults: 10,
      // Whether to split into separate index files
      separateTabs: false,
    },
  ],
],

// Add to the presets array (if using the docs preset):
presets: [
  [
    'classic',
    /** @type {import('@docusaurus/preset-classic').Options} */
    ({
      docs: {
        sidebarPath: require.resolve('./sidebars.js'),
        // Please change this to your repo.
        editUrl: 'https://github.com/your-org/physical-ai-docs/edit/main/',
        remarkPlugins: [
          require('remark-math'),
          require('mdx-mermaid')
        ],
        rehypePlugins: [
          require('rehype-katex')
        ],
      },
      blog: false, // Disable blog if not needed
      theme: {
        customCss: require.resolve('./src/css/custom.css'),
      },
    }),
  ],
],

// Additional configuration options to add to the main config object:
customFields: {
  // Book-specific metadata
  bookTitle: 'Physical AI & Humanoid Robotics',
  bookSubtitle: 'A Comprehensive Guide to Embodied Intelligence',
  bookAuthors: ['Author Name'],
  bookVersion: '1.0.0',
  bookPublishedDate: '2025-01-01',
  bookLicense: 'CC BY-NC 4.0',
},

// Additional plugin configuration:
plugins: [
  // Plugin for syntax highlighting extensions
  [
    '@docusaurus/plugin-content-blog',
    {
      id: 'code-blocks',
      path: 'code-examples',
      routeBasePath: 'code-examples',
    },
  ],
  // Plugin for image zoom
  [
    'docusaurus-plugin-image-zoom',
    {
      selector: '.markdown img',
      config: {
        background: 'rgba(0,0,0,0.8)',
        scrollOffset: 100,
        zIndex: 10000,
      },
    },
  ],
],

// Additional theme configuration:
themeConfig:
  /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
  ({
    // ... existing theme config

    // Mermaid diagram support
    mermaid: {
      options: {
        maxTextSize: 10000,
        fontFamily: 'var(--ifm-font-family-base)',
      },
    },

    // Algolia search configuration (alternative to local search)
    algolia: {
      // The application ID provided by Algolia
      appId: 'YOUR_APP_ID',
      // Public API key: it is safe to commit it
      apiKey: 'YOUR_SEARCH_API_KEY',
      indexName: 'physical-ai-humanoid-robotics',
      contextualSearch: true,
      searchPagePath: 'search',
    },

    // Metadata for social sharing
    metadata: [
      {
        name: 'keywords',
        content: 'physical ai, humanoid robotics, embodied intelligence, robotics, artificial intelligence, machine learning'
      },
      {
        name: 'twitter:card',
        content: 'summary_large_image'
      },
      {
        name: 'twitter:site',
        content: '@your_handle'
      },
    ],
  }),