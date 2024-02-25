"use client";

import Link from "next/link";
import { Button } from "@material-tailwind/react";
import { DarkContext } from "./Contexts";
import { useContext } from "react";

interface WebLinkProps {
  title: string;
  href: string;
  delay: string;
}

function WebLink({ title, href, delay }: WebLinkProps) {
  const isDark = useContext(DarkContext);
  return (
    <Link
      href={href}
      target="_blank"
      style={{ animationDelay: delay }}
      className="transition-color duration-500 opacity-0 animate-fadeIn"
    >
      <Button
        placeholder={undefined}
        variant="text"
        color="white"
        className="relative transition-shadow duration-200 rounded-2xl my-2 p-4 flex flex-col w-full h-full text-left hover:shadow-lg "
      >
        {isDark && (
          <div className="absolute transition-opacity duration-200 top-0 left-0 w-full h-full rounded-2xl bg-white opacity-5 hover:opacity-10"></div>
        )}
        <span
          className={
            "max-h-8 transition-color duration-500 font-quicksand font-bold text-lg overflow-hidden text-ellipsis " +
            (isDark ? "text-white" : "text-black")
          }
        >
          {title}
        </span>
        <span className="max-h-8 max-w-full pt-2 text-gray-500 font-quicksand font-semibold overflow-hidden text-ellipsis">
          {href}
        </span>
      </Button>
    </Link>
  );
}

export default WebLink;
