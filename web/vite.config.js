import { defineConfig } from 'vite';

export default defineConfig({
  base: '/CausalWorld/',
  build: {
    target: 'es2022',
    sourcemap: false,
    cssCodeSplit: true,
  },
});
