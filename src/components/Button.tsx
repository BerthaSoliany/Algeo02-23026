import React from 'react';

interface ButtonProps {
    text : string
}

function Button({text} : ButtonProps) {
  return (
    <div>
        <button className="bg-gray-800 hover:bg-white text-white hover:text-black font-bold py-1 px-2 w-[130px] rounded">
            {text}
        </button>
    </div>
  );
}

export default Button