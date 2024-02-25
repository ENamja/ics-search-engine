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
  const [errored, setErrored] = useState(false);
  const [linkArr, setLinkArr] = useState(Array<Array<string>>());
  const [rendered, setRendered] = useState(false);
  const [none, setNone] = useState(false);
  const delay = prevQuery == "" ? 1000 : 50;

  useEffect(() => {
    setPrevQuery(query);
    setLoading(true);
    setErrored(false);
    const getLinks = async () => {
      try {
        setLinkArr(Array<Array<string>>());
        const links = await getSearchResults({ query, length });
        setLinkArr(links);
        setRendered(true);
        if (links.length > 0) {
          setNone(false);
        } else {
          setNone(true);
        }
      } catch (error) {
        setErrored(true);
        console.log("There was an error", error);
      }
    };
    if (query) {
      getLinks();
    }
    setLoading(false);
  }, [query]);

  return (
    <div className="mb-16">
      {!loading && errored && <p>Failed to fetch</p>}
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
          {loading && !errored && <p>Loading...</p>}
        </div>
      )}
    </div>
  );
}

export default SearchResult;
