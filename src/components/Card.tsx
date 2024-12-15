import React from 'react';

interface CardProps {
    title: string;
    description: string;
    }

function Card({ title, description }: CardProps) {
  return (
    <div className="mt-5 mx-auto bg-black bg-opacity-50 py-10 px-5 rounded-3xl text-sm text-center max-w-[550px] space-y-5">
        <h1 className="font-bold text-white text-2xl">{title}</h1>
        <p className="text-white">{description}</p>
    </div>
  );
}

export default Card