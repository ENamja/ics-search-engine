/** @type {import('next').NextConfig} */
// const nextConfig = require('@next/bundle-analyzer')({
//   enabled: process.env.ANALYZE === 'true',
//   rewrites: async () => {
//     return [
//       {
//         source: "/api/:path*",
//         destination:
//           process.env.NODE_ENV === "development"
//             ? "http://127.0.0.1:8080/api/search/:path*"
//             : "/api/search/",
//       },
//     ];
//   },
//   reactStrictMode: true,
// });

const nextConfig = {
  enabled: process.env.ANALYZE === 'true',
  rewrites: async () => {
    return [
      {
        source: "/api/:path*",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://127.0.0.1:8080/api/search/:path*"
            : "/api/search/",
      },
    ];
  },
  reactStrictMode: true,
};

module.exports = nextConfig;
