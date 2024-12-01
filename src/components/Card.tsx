import React from 'react';

interface CardProps {
    title: string;
    description: string;
    }

function Card({ title, description }: CardProps) {
  return (
    <div className="mt-5 mx-auto bg-gray-700 py-1 px-2 rounded-sm text-lg text-center max-w-[550px]">
        <h1 className="font-bold text-yellow-400 text-3xl mt-5 mb-2">{title}</h1>
        <p className="text-white mt-5">{description}</p>
    </div>
  );
}

export default Card