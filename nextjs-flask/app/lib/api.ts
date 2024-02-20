"use server";

interface getSearchResultsProps {
  query: string;
  length: number;
}

export async function getSearchResults({
  query,
  length,
}: getSearchResultsProps) {
  const host = process.env.NEXT_PUBLIC_HOST;
  const api_port = process.env.API_PORT;

  console.log(
    `LIB API: http://${host}:${api_port}/api/home?query=${query}&length=${length}`
  );
  const res = await fetch(
    `http://${host}:${api_port}/api/home?query=${query}&length=${length}`
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
  return [];
}
