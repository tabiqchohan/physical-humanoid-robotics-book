import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import type { Config } from '@docusaurus/types';
import { themes as prismThemes } from 'prism-react-renderer';




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
          path: 'docs',
          include: ['**/*.md', '**/*.mdx'], // Include all markdown files
          exclude: [], // Don't exclude any files for now
        },
        blog: false, // Disable blog to reduce memory usage
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
        sitemap: {
          changefreq: 'weekly',
          priority: 0.5,
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
  theme: prismThemes.github,
  darkTheme: prismThemes.dracula,
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

  },

markdown: {
  hooks: {
    onBrokenMarkdownImages: 'warn',
    onBrokenMarkdownLinks: 'warn',
  },
},


  // Optimize memory usage
  trailingSlash: true,
  onBrokenLinks: 'warn',

  themes: [
    '@docusaurus/theme-mermaid',
  ],

  plugins: [
    [require.resolve('docusaurus-plugin-image-zoom'), {}],
    [
      '@docusaurus/plugin-client-redirects',
      {
        redirects: [
          {
            to: '/',
            from: ['/chat'], // In case we want to have a dedicated chat page
          },
        ],
      },
    ],
  ],

  themes: [
    '@docusaurus/theme-mermaid',
  ],

  clientModules: [
    require.resolve('./src/Root.tsx'),
  ],

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
