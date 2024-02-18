"use client";

import Toggle from "./ToggleTheme";
import { Dispatch, SetStateAction } from "react";
import Link from "next/link";

interface NavBarProps {
  dark: boolean;
  setDark: Dispatch<SetStateAction<boolean>>;
}

function NavBar({ dark, setDark }: NavBarProps) {
  return (
    <div
      className={
        "transition-color duration-500 fixed top-0 left-0 w-screen h-24 flex justify-center items-center z-[100] " +
        (dark ? "text-white bg-[#121212]" : "text-blue-700 bg-white")
      }
    >
      <Link href="/" className="font-quicksand font-extrabold text-5xl">
        UCI ICS Search Engine
      </Link>
      <div className="fixed right-8">
        <Toggle dark={dark} setDark={setDark}></Toggle>
      </div>
    </div>
  );
}

export default NavBar;
