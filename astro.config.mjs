import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwind from '@astrojs/tailwind';

// https://astro.build/config
export default defineConfig({
  site: 'https://saint2706.github.io',
  base: '/scroll-of-dharma',
  integrations: [mdx(), tailwind()],
  markdown: {
    shikiConfig: {
      theme: 'dracula',
    },
  },
});
