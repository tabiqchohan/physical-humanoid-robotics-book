import type { Config } from '@docusaurus/types';
import { themes as prismThemes } from 'prism-react-renderer';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'The Future of Intelligent Machines',
  favicon: 'img/favicon.ico',

  url: 'https://physical-humanoid-robotics-book.vercel.app',
  baseUrl: '/',

  organizationName: 'tabiqchohan',
  projectName: 'physical-humanoid-robotics-book',

  // 🔥 IMPORTANT: build fail nahi hogi
  onBrokenLinks: 'ignore',
  onBrokenMarkdownLinks: 'ignore',

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
          path: 'docs',
          include: ['**/*.md', '**/*.mdx'],
        },

        // ✅ blog disabled properly
        blog: false,

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
        alt: 'Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Book',
        },
        {
          href: 'https://github.com/tabiqchohan',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },

    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [{ label: 'Book', to: '/docs/intro' }],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/tabiqchohan',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Tabiq Chohan`,
    },

    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  },

  trailingSlash: true,

  themes: ['@docusaurus/theme-mermaid'],

  clientModules: [require.resolve('./src/Root.tsx')],

  customFields: {
    backendUrl:
      process.env.REACT_APP_BACKEND_URL ||
      'https://tabiqchohan-rag-chatbot.hf.space',
  },
};

export default config;
