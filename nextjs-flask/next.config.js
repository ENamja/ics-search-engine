/** @type {import('next').NextConfig} */
const nextConfig = {
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
  env: {
    BASE_URL: process.env.BASE_URL,
    PORT: process.env.PORT,
  },
};

module.exports = nextConfig;
