import { context } from 'esbuild';
import { sassPlugin } from 'esbuild-sass-plugin';

const watch = process.argv.includes("--watch");
const env = process?.env?.NODE_ENV ?? JSON.stringify("production");

const ctx = await context({
  entryPoints: ['./mextmock-ui/index.tsx'],
  outdir: './static',
  bundle: true,
  platform: 'browser',
  mainFields: ["browser", "module", "main"],
  format: 'esm',
  sourcemap: true,
  allowOverwrite: true,
  define: {
    "process.env.NODE_ENV": env,
  },
  plugins: [sassPlugin({
    filter: /\.scss$/,
    type: 'style',
    loadPaths: ['./node_modules'],
  })],
});

if (watch) {
  await ctx.watch();
  console.log('watching...');
} else {
  await ctx.rebuild();
  await ctx.dispose();
}

