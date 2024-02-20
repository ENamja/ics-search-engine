"use client";

import WebLink from "./WebLink";
import { useState, useEffect, useContext } from "react";
import { QueryContext, LengthContext } from "./Contexts";
import { getSearchResults } from "./lib/api";

function SearchResult() {
  const query = useContext(QueryContext);
  const length = useContext(LengthContext);
  const [prevQuery, setPrevQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [linkArr, setLinkArr] = useState(Array<Array<string>>());
  const [rendered, setRendered] = useState(false);
  const [errored, setErrored] = useState(false);
  const [none, setNone] = useState(false);
  const delay = prevQuery == "" ? 1000 : 50;
  const host = process.env.BASE_URL;
  const port = process.env.PORT;

  useEffect(() => {
    setErrored(false);
    setPrevQuery(query);
    setLoading(true);
    if (query) {
      console.log(`SEARCHRESULT: ${host}, ${port}`);
      getSearchResults({ query, length })
        .then((response) => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error("Failed to fetch");
          }
        })
        .then((data) => {
          let links = Array<Array<string>>();
          const keys = Object.keys(data.result).length;
          for (let i = 0; i < keys; i++) {
            links.push(data.result[i]);
          }
          if (links.length == 0) {
            setNone(true);
          } else {
            setNone(false);
          }
          setLinkArr(links);
          setRendered(true);
        })
        .catch((e) => {
          setErrored(true);
        });
    }
    setLoading(false);
  }, [query]);

  return (
    <div className="mb-16">
      {!loading && errored && <p>Failed to fetch data</p>}
      {!loading && !errored && none && <p>No results</p>}
      {!loading && !errored && rendered && (
        <div className="flex flex-col w-full">
          {linkArr.map((i, index) => {
            return (
              <>
                <WebLink
                  key={index}
                  href={String(i[0])}
                  title={String(i[1])}
                  delay={`${(index + 1) * 100 + delay}ms`}
                ></WebLink>
              </>
            );
          })}
          {loading && <p>Loading...</p>}
        </div>
      )}
    </div>
  );
}

export default SearchResult;
