import { NextResponse } from "next/server";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get("query");
  const length = searchParams.get("length");
  const host = process.env.NEXT_PUBLIC_HOST;
  const api_port = process.env.API_PORT;

  try {
    if (!query) {
      throw new Error("Query required");
    }

    console.log(
      `ROUTE API: http://${host}:${api_port}/api/home?query=${query}&length=${length}`
    );

    const res = await fetch(
      `http://${host}:${api_port}/api/home?query=${query}&length=${length}`
    );
    if (!res.ok) {
      throw new Error(`Failed to fetch data`);
    }
    const jsonObj = await res.json();
    const result = jsonObj.result;
    return NextResponse.json({ result }, { status: 200 });
  } catch (error) {
    if (error instanceof Error) {
      return NextResponse.json({ error: error.message }, { status: 400 });
    } else {
      return NextResponse.json(
        { error: "error is not type Error" },
        { status: 500 }
      );
    }
  }
}
