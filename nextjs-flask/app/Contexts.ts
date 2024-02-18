"use client";

import { createContext } from "react";

const DarkContext = createContext(true);
const QueryContext = createContext("");
const LengthContext = createContext(10);

export { DarkContext, QueryContext, LengthContext };
