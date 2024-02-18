"use client";

import { Button } from "@material-tailwind/react";
import { Dispatch, SetStateAction, useState } from "react";

interface ToggleLengthProps {
  length: number;
  setLength: Dispatch<SetStateAction<number>>;
}

function ToggleLength({ length, setLength }: ToggleLengthProps) {
  function decrementLength() {
    if (length > 1) {
      setLength(length - 1);
    }
  }
  function incrementLength() {
    setLength(length + 1);
  }

  return (
    <div className="flex flex-row items-center my-auto mx-3 font-normal text-gray-500 rounded-lg">
      <Button
        className="w-6 h-6 text-2xl font-normal text-center flex justify-center items-center"
        variant="text"
        color="gray"
        onClick={decrementLength}
        placeholder={undefined}
      >
        <span>-</span>
      </Button>
      <span className="mx-2 w-6">{length}</span>
      <Button
        className="font-normal w-6 h-6 text-2xl text-center flex justify-center items-center"
        variant="text"
        color="gray"
        onClick={incrementLength}
        placeholder={undefined}
      >
        <span>+</span>
      </Button>
    </div>
  );
}

export default ToggleLength;
