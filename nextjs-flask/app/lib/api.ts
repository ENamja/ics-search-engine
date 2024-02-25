"use server";

interface getSearchResultsProps {
  query: string;
  length: number;
}

export async function getSearchResults({
  query,
  length,
}: getSearchResultsProps) {
  const host = process.env.HOST;
  const port = process.env.PORT;

  try {
    const res = await fetch(
      `http://${host}:${port}/api?query=${query}&length=${length}`
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
    throw new Error("Failed to fetch");
  }
}
