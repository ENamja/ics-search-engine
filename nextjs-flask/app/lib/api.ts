"use server";

interface getSearchResultsProps {
  query: string;
  length: number;
}

export async function getSearchResults({
  query,
  length,
}: getSearchResultsProps) {
  const base_url = process.env.BASE_URL;
  const port = process.env.PORT;

  console.log(
    `LIB API: http://${base_url}:${port}/api?query=${query}&length=${length}`
  );
  const res = await fetch(
    `http://${base_url}:${port}/api?query=${query}&length=${length}`
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
