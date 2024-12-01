import Button from '@/src/components/Button';
import ImageCard from '@/src/components/ImageCard';
import NavBar from '@/src/components/NavBar';
import React from 'react'

function Album() {
  return (
    <div className="bg-[url('/bg.png')] bg-cover bg-center min-h-screen flex flex-col">
      <NavBar />
      <div className="flex flex-row space-x-5 ml-10 mr-10">
        <div className="mt-5 bg-white rounded-md py-2 px-2 w-[90%] md:w-[450px] h-auto flex flex-col items-center">
          {/* komponen imagecard yg ini harus sesuai dgn file yg di up */}
          <ImageCard 
            image="ash.png"
            text="image.png"
          />
          <div className="mt-5 mb-5 space-y-2">
            <Button
              text="Upload Dataset"
            />
            <Button
              text="Upload Mapper"
            />
            <Button
              text="Upload File"
            />
          </div>
          <p className="text-black">Dataset Name : </p>
          <p className="text-black">Mapper Name : </p>
          <p className="text-black">File Name : </p>
        </div>
        <div className="mt-5 bg-white rounded-md py-2 px-2 w-[90%] md:w-full h-auto">
          <div className="flex flex-row justify-center items-center mt-1 space-x-5">
            <Button 
              text="Album"
            />
            <Button
              text="Music"
            />
          </div>
          <div className="flex flex-row justify-center items-center mt-1 space-x-5">
            <ImageCard
              image="ash.png"
              text="image.png"
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Album;