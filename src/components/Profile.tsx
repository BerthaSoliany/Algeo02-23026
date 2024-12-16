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
    <div className="relative bg-black bg-opacity-50 rounded-3xl px-10 py-5 max-w-[90%] md:max-w-[800px] font-custom">
        <img className="absolute left-28 bottom-2 md:left-52 md:-bottom-3 w-[18%] md:w-[13%] h-auto" src={image1}/>
        <div className="flex flex-row justify-center items-center space-x-20">
            <img className="w-[30%] h-auto rounded-full" src={image2}/>
            <div className="flex flex-col space-y-5">
                <h1 className="font-bold text-white text-xl">{name}</h1>
                <p className="text-white text-lg">{nim}</p>
                <p className="text-white text-sm">Kata-kata untuk tubes ini:<br/>{quote}</p>
            </div>
        </div>
    </div>
  );
}

export default Profile