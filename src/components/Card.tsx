import React from 'react';

interface CardProps {
    title: string;
    description: string;
    }

function Card({ title, description }: CardProps) {
  return (
    <div className="mt-5 mx-auto bg-black bg-opacity-50 py-1 px-2 rounded-md text-sm text-center max-w-[550px]">
        <h1 className="font-bold text-white text-2xl mt-5 mb-2">{title}</h1>
        <p className="text-white mt-5">{description}</p>
    </div>
  );
}

export default Card