import React from 'react';

interface ProfileProps {
    image1: string;
    image2: string;
    name: string;
    nim: string;
    quote: string;
}

function Profile({ image1, image2, name, nim, quote }: ProfileProps) {
  return (
    <div className="relative bg-black bg-opacity-50 rounded-xl px-2 py-2 max-w-[90%] md:max-w-[800px] mx-auto mt-10 font-custom">
        <img className="absolute left-28 bottom-2 md:left-52 md:-bottom-3 w-[18%] md:w-[16%] h-auto" src={image1}/>
        <div className="flex flex-row justify-center items-center space-x-20">
            <img className="w-[30%] h-auto rounded-full" src={image2}/>
            <div className="flex flex-col">
                <h1 className="font-bold text-white text-xl mt-2 mb-2">{name}</h1>
                <p className="text-white text-lg mt-2 mb-5">{nim}</p>
                <p className="text-white mt-2 text-sm">Kata-kata untuk tubes ini:<br/>{quote}</p>
            </div>
        </div>
    </div>
  );
}

export default Profile