import type { Config } from '@docusaurus/types';
import { themes as prismThemes } from 'prism-react-renderer';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'A Comprehensive Guide to Embodied Intelligence',
  favicon: 'img/favicon.ico',

  url: 'https://physical-humanoid-robotics-book.vercel.app',
  baseUrl: '/',

  organizationName: 'tabiqchohan',
  projectName: 'physical-humanoid-robotics-book',

  onBrokenLinks: 'ignore',
  onBrokenMarkdownLinks: 'ignore',

  i18n: { defaultLocale: 'en', locales: ['en'] },

  // Merge all presets into one array
  presets: [
    [
      'classic',
      {
        docs: {
          id: 'physical-ai-docs',
          path: 'docs',
          routeBasePath: 'docs',
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/your-org/physical-ai-docs/edit/main/',
          remarkPlugins: [require('remark-math'), require('mdx-mermaid')],
          rehypePlugins: [require('rehype-katex')],
        },
        blog: false,
        theme: { customCss: require.resolve('./src/css/custom.css') },
      },
    ],
  ],

  themes: [
    '@docusaurus/theme-mermaid',
    [
      require.resolve('@easyops-cn/docusaurus-search-local'),
      {
        indexDocs: true,
        indexBlog: false,
        indexPages: false,
        language: ['en'],
        placeholder: 'Search Physical AI & Humanoid Robotics docs...',
        maxSearchResults: 10,
        separateTabs: false,
      },
    ],
  ],

  plugins: [
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
    [
      '@docusaurus/plugin-content-blog',
      {
        id: 'code-blocks',
        path: 'code-examples',
        routeBasePath: 'code-examples',
      },
    ],
    [
      'docusaurus-plugin-image-zoom',
      {
        selector: '.markdown img',
        config: { background: 'rgba(0,0,0,0.8)', scrollOffset: 100, zIndex: 10000 },
      },
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: { alt: 'Logo', src: 'img/logo.svg' },
      items: [
        { type: 'docSidebar', sidebarId: 'tutorialSidebar', position: 'left', label: 'Book' },
        { href: 'https://github.com/tabiqchohan', label: 'GitHub', position: 'right' },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        { title: 'Docs', items: [{ label: 'Book', to: '/docs/intro' }] },
        { title: 'Community', items: [{ label: 'GitHub', href: 'https://github.com/tabiqchohan' }] },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Tabiq Chohan`,
    },
    prism: { theme: prismThemes.github, darkTheme: prismThemes.dracula },
    mermaid: { options: { maxTextSize: 10000, fontFamily: 'var(--ifm-font-family-base)' } },
    algolia: {
      appId: 'YOUR_APP_ID',
      apiKey: 'YOUR_SEARCH_API_KEY',
      indexName: 'physical-ai-humanoid-robotics',
      contextualSearch: true,
      searchPagePath: 'search',
    },
    metadata: [
      { name: 'keywords', content: 'physical ai, humanoid robotics, embodied intelligence, robotics, artificial intelligence, machine learning' },
      { name: 'twitter:card', content: 'summary_large_image' },
      { name: 'twitter:site', content: '@your_handle' },
    ],
  },

  trailingSlash: true,

  clientModules: [require.resolve('./src/Root.tsx')],

  customFields: {
    bookTitle: 'Physical AI & Humanoid Robotics',
    bookSubtitle: 'A Comprehensive Guide to Embodied Intelligence',
    bookAuthors: ['Author Name'],
    bookVersion: '1.0.0',
    bookPublishedDate: '2025-01-01',
    bookLicense: 'CC BY-NC 4.0',
  },
};

export default config;
