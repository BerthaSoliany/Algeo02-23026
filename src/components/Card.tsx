import React from 'react';

interface CardProps {
    title: string;
    description1: string;
    description2: string;
    description3: string;
    description4: string;
    description5?: string;

    }

function Card({ title, description1, description2, description3, description4, description5 }: CardProps) {
  return (
    <div className="mt-5 mx-auto bg-black bg-opacity-50 py-10 px-5 rounded-3xl text-sm text-center max-w-[550px] space-y-5">
        <h1 className="font-bold text-white text-2xl">{title}</h1>
        <p className="text-white">{description1}</p>
        <p className="text-white">{description2}</p>
        <p className="text-white">{description3}</p>
        <p className="text-white">{description4}</p>
        <p className="text-white">{description5}</p>
    </div>
  );
}

export default Card