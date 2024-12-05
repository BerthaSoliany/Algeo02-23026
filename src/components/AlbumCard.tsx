import React from 'react';

interface AlbumCardProps {
    image : string
    name : string
}

function AlbumCard({ image, name} : AlbumCardProps ) {
  return (
    <div className="flex flex-col space-y-1 items-center">
        <div className="w-[160px] h-[100px] p-2 bg-gray-800 rounded-md flex items-center justify-center">
          <img src={image} className="w-full h-full object-contain" alt={name} />
        </div>
        <p className="text-white text-[11px] truncate overflow-hidden text-ellipsis whitespace-nowrap w-[150px]">{name}</p>
    </div>
  );
}

export default AlbumCard