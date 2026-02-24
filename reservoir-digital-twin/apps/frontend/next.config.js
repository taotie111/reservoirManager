// ES module Next.js config (compatible with package.json "type": "module")
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  eslint: {
    ignoreDuringBuilds: true,
  },
  i18n: {
    locales: ['en'],
    defaultLocale: 'en',
  },
  images: {
    unoptimized: true
  }
};

export default nextConfig;
