import { rmSync } from 'node:fs';
import path from 'node:path';
import { context } from 'esbuild';
import { sassPlugin } from 'esbuild-sass-plugin';

const watch = process.argv.includes("--watch");
const env = JSON.stringify(process.env.NODE_ENV ?? 'production');
const outdir = path.resolve('./static');

rmSync(outdir, { recursive: true, force: true });

const ctx = await context({
  entryPoints: [
    './mextmock-ui/configure.tsx',
    './mextmock-ui/get-one.tsx',
    './mextmock-ui/history.tsx',
    './mextmock-ui/modal.tsx',
  ],
  outdir,
  bundle: true,
  platform: 'browser',
  mainFields: ["browser", "module", "main"],
  format: 'iife',
  sourcemap: true,
  allowOverwrite: true,
  define: {
    "process.env.NODE_ENV": env,
  },
plugins: [sassPlugin({
  filter: /\.scss$/,
  type: 'style',
  loadPaths: ['node_modules'],
})],
});

if (watch) {
  await ctx.watch();
  console.log('watching...');
} else {
  await ctx.rebuild();
  await ctx.dispose();
}

