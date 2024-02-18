"use client";

import "./styles/globals.css";
import NavBar from "./NavBar";
import SearchBar from "./SearchBar";
import { DarkContext, QueryContext, LengthContext } from "./Contexts";
import { useState } from "react";
import { Quicksand } from "next/font/google";

const quicksand = Quicksand({
  subsets: ["latin"],
  variable: "--font-quicksand",
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [dark, setDark] = useState(false);
  const [query, setQuery] = useState("");
  const [length, setLength] = useState(10);
  return (
    <html lang="en" className={quicksand.variable}>
      <body
        className={
          "duration-500 flex flex-col font-quicksand items-center text-center w-screen min-h-screen h-full " +
          (dark ? "bg-[#121212] text-white" : "bg-white text-black")
        }
      >
        <DarkContext.Provider value={dark}>
          <NavBar dark={dark} setDark={setDark}></NavBar>
          <QueryContext.Provider value={query}>
            <LengthContext.Provider value={length}>
              <div className="w-2/5 min-h-screen flex flex-col justify-center items-center py-24 mx-auto relative">
                <SearchBar
                  query={query}
                  setQuery={setQuery}
                  length={length}
                  setLength={setLength}
                ></SearchBar>
                {children}
              </div>
            </LengthContext.Provider>
          </QueryContext.Provider>
        </DarkContext.Provider>
      </body>
    </html>
  );
}
