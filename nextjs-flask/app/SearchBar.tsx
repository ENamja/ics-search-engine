"use client";

import { useState, Dispatch, SetStateAction } from "react";
import ToggleLength from "./ToggleLength";

interface SearchBarProps {
  query: string;
  setQuery: Dispatch<SetStateAction<string>>;
  length: number;
  setLength: Dispatch<SetStateAction<number>>;
}

function SearchBar({ query, setQuery, length, setLength }: SearchBarProps) {
  const [hasSearched, setHasSearched] = useState(false);
  const [search, setSearch] = useState("");

  function handleForm() {
    setHasSearched(true);
    setQuery(search);
  }

  return (
    <div
      className={
        "transition-all duration-500 absolute z-10 flex flex-row " +
        (hasSearched ? "animate-moveSearch" : "bottom-1/2 translate-y-1/2")
      }
    >
      <form action={handleForm} method={undefined}>
        <input
          type="search"
          placeholder="Search Here"
          required
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
          }}
          className="rounded-3xl h-12 w-96 p-4 text-black my-8 mx-3 z-10"
        />
      </form>
      <ToggleLength length={length} setLength={setLength}></ToggleLength>
    </div>
  );
}

export default SearchBar;
