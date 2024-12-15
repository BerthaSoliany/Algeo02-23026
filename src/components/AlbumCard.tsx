import React from 'react';

interface AlbumCardProps {
    image : string
    name : string
    similarity : number
}

function AlbumCard({ image, name, similarity } : AlbumCardProps ) {
  return (
    <div className="flex flex-col space-y-1 items-center">
        <div className="w-[160px] h-[100px] p-5 bg-gray-800 rounded-md flex items-center justify-center">
          <a href="/album">
            <img src={image} className="w-full h-full object-contain" alt={name} />
          </a>
        </div>
        <p className="text-white text-[11px] truncate overflow-hidden text-ellipsis whitespace-nowrap w-[150px]">{name}</p>
        <p className="text-white text-[8px] truncate overflow-hidden text-ellipsis whitespace-nowrap w-[150px]">{similarity}%</p>
    </div>
  );
}

export default AlbumCard