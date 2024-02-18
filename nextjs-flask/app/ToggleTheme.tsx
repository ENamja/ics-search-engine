"use client";

import { Dispatch, SetStateAction } from "react";

interface ToggleProps {
  dark: boolean;
  setDark: Dispatch<SetStateAction<boolean>>;
}

function handleChange({ dark, setDark }: ToggleProps) {
  setDark(!dark);
}

function Toggle({ dark, setDark }: ToggleProps) {
  return (
    <>
      <input
        className="w-0 h-0 hidden z-[100]"
        type="checkbox"
        id="toggle"
        onChange={() => handleChange({ dark, setDark })}
      />
      <label
        className={
          "duration-500 w-14 h-8 z-[100] relative block rounded-2xl cursor-pointer after:content-[''] after:w-6 after:h-6 after:absolute \
              after:top-1 after:left-1 after:bg-gradient-to-b after:rounded-[12px] after:duration-500 after:transition-all" +
          (dark
            ? " shadow-[inset_0_-1.5px_3px_rgba(255,255,255,0.4)] after:from-[#777] after:to-[#3a3a3a] bg-[#242424]"
            : " shadow-[inset_0_1.5px_3px_rgba(0,0,0,0.4)] after:from-[#ffffff] after:to-[#e0e0e0] after:translate-x-[100%] bg-[#d4d4d4]")
        }
        htmlFor="toggle"
      ></label>
    </>
  );
}

export default Toggle;
