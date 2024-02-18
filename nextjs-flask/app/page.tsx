import { Metadata } from "next";
import SearchResult from "./SearchResult";

export const metadata: Metadata = {
  title: "Search Engine",
  description: "UCI ICS Subdomain Search Engine",
};

export default function Home() {
  return (
    <div className="absolute top-56 w-full">
      <SearchResult></SearchResult>
    </div>
  );
}
