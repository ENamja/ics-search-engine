/** @type {import('next').NextConfig} */
const { loadEnvConfig } = require("@next/env");
loadEnvConfig(".");
const nextConfig = {
  rewrites: async () => {
    return [
      {
        source: "/api/:path*",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://127.0.0.1:8080/api/:path*"
            : `http://${process.env['HOST']}:${process.env['API_PORT']}/api/:path*`,
            // : "/api/",
      },
    ];
  },
  reactStrictMode: true,
};

module.exports = nextConfig;
