import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import type { Config } from '@docusaurus/types';

// Prism themes
import githubTheme from 'prism-react-renderer/themes/github';
import draculaTheme from 'prism-react-renderer/themes/dracula';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'The Future of Intelligent Machines',
  favicon: 'img/favicon.ico',

  url: 'https://your-docusaurus-site.example.com',
  baseUrl: '/',

  organizationName: 'your-github-org',
  projectName: 'physical-ai-robotics',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          remarkPlugins: [remarkMath],
          rehypePlugins: [rehypeKatex],
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: {
          showReadingTime: true,
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',

    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'My Site Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Book',
        },
        { to: '/blog', label: 'Blog', position: 'left' },
        {
          href: 'https://github.com/facebook/docusaurus',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },

    footer: {
      style: 'dark',
      links: [
        { title: 'Docs', items: [{ label: 'Book', to: '/docs/intro' }] },
        {
          title: 'Community',
          items: [
            { label: 'Stack Overflow', href: 'https://stackoverflow.com/questions/tagged/docusaurus' },
            { label: 'Discord', href: 'https://discordapp.com/invite/docusaurus' },
            { label: 'Twitter', href: 'https://twitter.com/docusaurus' },
          ],
        },
        {
          title: 'More',
          items: [
            { label: 'Blog', to: '/blog' },
            { label: 'GitHub', href: 'https://github.com/facebook/docusaurus' },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} My Project, Inc. Built with Docusaurus.`,
    },

    prism: {
      theme: githubTheme,
      darkTheme: draculaTheme,
    },

    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: false,
    },

    docs: {
      versionPersistence: 'localStorage',
      sidebar: { hideable: false, autoCollapseCategories: false },
    },

    blog: { sidebar: { groupByYear: true } },

    metadata: [],

    tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },

    mermaid: { theme: { dark: 'dark', light: 'default' }, options: {} },

    // Algolia search plugin config with unique ID
    algolia: {
      appId: 'YOUR_APP_ID',
      apiKey: 'YOUR_SEARCH_API_KEY',
      indexName: 'YOUR_INDEX_NAME',
    },
  },

  markdown: {
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'warn', // deprecated replacement
      onBrokenMarkdownImages: 'warn', // ignore missing images
    },
  },

  themes: [
    '@docusaurus/theme-mermaid',
    [
      '@docusaurus/theme-search-algolia',
      {
        id: 'default-search', // unique plugin ID
        algolia: {
          appId: 'YOUR_APP_ID',
          apiKey: 'YOUR_SEARCH_API_KEY',
          indexName: 'YOUR_INDEX_NAME',
        },
      },
    ],
  ],

  plugins: [[require.resolve('docusaurus-plugin-image-zoom'), {}]],

  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.13.11/dist/katex.min.css',
      integrity:
        'sha384-Um5gpz1odJg5bR4acIgFfFYsebxPIRVkeMmKcVwLWeMyNDxUHWahFqDNTPYLt2VBL',
      crossorigin: 'anonymous',
    },
  ],
};

export default config;
