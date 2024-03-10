"use server";

import { headers } from "next/headers";

interface getSearchResultsProps {
  query: string;
  length: number;
}

export async function getSearchResults({
  query,
  length,
}: getSearchResultsProps) {
  const headersList = headers();
  let host = headersList.get("host");
  const port = process.env["API_PORT"];

  try {
    if (host && host.includes(":")) {
      // Getting rid of port in host if it is included
      const index = host.indexOf(":");
      host = host.substring(0, index);
    }
    console.log(
      `http://${host}:${port}/api/search?query=${query}&length=${length}`
    );
    const res = await fetch(
      `http://${host}:${port}/api/search?query=${query}&length=${length}`
    );
    if (res.ok) {
      const data = await res.json();
      let links = Array<Array<string>>();
      const keys = Object.keys(data.result).length;
      for (let i = 0; i < keys; i++) {
        links.push(data.result[i]);
      }
      return links;
    }
    throw new Error(`${res.status} ${res.statusText}`);
  } catch (error) {
    console.log(error);
    throw new Error("Failed to fetch");
  }
}
