import React from 'react';

interface ImageCardProps {
    image : string
    text : string
}

function ImageCard({image, text} : ImageCardProps) {
  return (
    <div className="flex flex-col space-y-1 items-center">
        <img src={image} className="w-[30%] h-auto"/>
        <p className="text-black">{text}</p>
    </div>
  );
}

export default ImageCard