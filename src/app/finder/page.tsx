"use client";
import Button from '@/src/components/Button';
import AlbumCard from '@/src/components/AlbumCard';
import MusicCard from '@/src/components/MusicCard';
import NavBar from '@/src/components/NavBar';
import React, { useState } from 'react';


function Album() {
  const [activeButton, setActiveButton] = useState<'album' | 'music' | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [uploadedFileName, setUploadedFileName] = useState<string | null>(null);
  const [datasetFileName, setDatasetFileName] = useState<string | null>(null);
  const [mapperFileName, setMapperFileName] = useState<string | null>(null);
  const [uploadedImageUrl, setUploadedImageUrl] = useState<string | null>(null);
  const itemsPerPage = 10;

  const handleButtonClick = (button: 'album' | 'music') => {
    setActiveButton(button);
    setCurrentPage(1);
  };


  const albumData = [
    { image: '/path/to/album1.jpg', name: 'Album 1', audioSrc: '/path/to/album1.mp3' },
    { image: '/path/to/album2.jpg', name: 'Album 2', audioSrc: '/path/to/album2.mp3' },
    { image: '/path/to/album3.jpg', name: 'Album 3', audioSrc: '/path/to/album3.mp3' },
    { image: '/path/to/album4.jpg', name: 'Album 4', audioSrc: '/path/to/album4.mp3' },
    { image: '/path/to/album5.jpg', name: 'Album 5', audioSrc: '/path/to/album5.mp3' },
    { image: '/path/to/album6.jpg', name: 'Album 6', audioSrc: '/path/to/album6.mp3' },
    // Add more album data
  ];

  const musicData = [
    { image: '/path/to/music1.jpg', name: 'Music 1', audioSrc: 'public/../I_Want_It_That_Way.mid' },
    { image: '/path/to/music1.jpg', name: 'Music 2', audioSrc: './public/town-10169.mp3' },
    { image: '/path/to/music1.jpg', name: 'Music 3', audioSrc: '/town-10169.mp3' },
    { image: '/path/to/music1.jpg', name: 'Music 4', audioSrc: './town-10169.mp3' },
    { image: '/path/to/music1.jpg', name: 'Music 5', audioSrc: '../town-10169.mp3' },
    { image: '/path/to/music1.jpg', name: 'Music 6', audioSrc: 'public/../town-10169.mp3' },
    { image: '/path/to/music1.jpg', name: 'Music 7', audioSrc: '/path/to/music1.mp3' },
    { image: '/path/to/music1.jpg', name: 'Music 8', audioSrc: '/path/to/music1.mp3' },
    { image: '/path/to/music1.jpg', name: 'Music 9', audioSrc: '/path/to/music1.mp3' },
    { image: '/path/to/music1.jpg', name: 'Music 10', audioSrc: '/path/to/music1.mp3' },
    { image: '/path/to/music1.jpg', name: 'Music 11', audioSrc: '/path/to/music1.mp3' },
    { image: '/path/to/music1.jpg', name: 'Music 12', audioSrc: '/path/to/music1.mp3' },

    // Add more music data
  ];

  const currentData = activeButton === 'album' ? albumData : activeButton === 'music' ? musicData : [];
  const totalPages = Math.ceil(currentData.length / itemsPerPage);

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handlePreviousPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = currentData.slice(indexOfFirstItem, indexOfLastItem);

  const handleFileChange = (file: File | null, type: 'upload' | 'dataset' | 'mapper') => {
    if (file) {
      if (type === "upload"){
        setUploadedFileName(file.name);
        // Check if the uploaded file is an image
        if (file.type.startsWith('image/')) {
          const url = URL.createObjectURL(file);
          setUploadedImageUrl(url);
        } else {
          setUploadedImageUrl(null);
        }
      } else if (type === "dataset"){
        setDatasetFileName(file.name);
      } else if (type === "mapper"){
        setMapperFileName(file.name);
      }
    }
  };
  
  return (
    <div className="bg-[url('/image1.png')] bg-cover bg-center min-h-screen flex flex-col p-2 md:p-4 font-custom">
      <NavBar />
      <div className="flex flex-col space-y-2 md:flex-row md:space-x-5 text-xs items-center">
        <div className="mt-2 bg-black bg-opacity-50 rounded-md py-2 px-2 w-[90%] md:max-w-[320px] h-auto md:h-[440px] flex flex-col justify-center items-center space-y-8">
          {/* komponen AlbumCard yg ini harus sesuai dgn file yg di up */}
          {/* ada 2 dataset yg di up audio/img */}
          {/* tambahin jg page lg di page brpnya */}
          {/* audio can be played */}
          {/* search dgn click album/music */}
          {/* mapper dibuat sendiri */}
          <div className="flex flex-col space-y-1 items-center">
            {uploadedImageUrl && (
              <div className="w-[240px] h-[140px] p-2 bg-gray-800 rounded-md flex items-center justify-center">
                <img src={uploadedImageUrl} alt="Uploaded" className="w-full h-full object-contain" />
              </div>
            )}
            {uploadedFileName && <p className="text-white text-[11px] truncate overflow-hidden text-ellipsis whitespace-nowrap w-[300px] text-center">{uploadedFileName}</p>}
          </div>
          <Button
            text="Upload"
            onFileChange={(file) => handleFileChange(file, "upload")}
          />
          <div className='flex flex-col items-center space-y-2'>
            <Button
              text="Upload Dataset"
              onFileChange={(file) => handleFileChange(file, 'dataset')}
            />
            {datasetFileName && <p className="text-white text-[11px] truncate overflow-hidden text-ellipsis whitespace-nowrap w-[300px] text-center">Dataset: {datasetFileName}</p>}
          </div>
          <div className='flex flex-col items-center space-y-2'>
            <Button
              text="Upload Mapper"
              onFileChange={(file) => handleFileChange(file, 'mapper')}
            />
            {mapperFileName && <p className="text-white text-[11px] truncate overflow-hidden text-ellipsis whitespace-nowrap w-[300px] text-center">Mapper: {mapperFileName}</p>}
          </div>
        </div>
        <div className="mt-2 bg-black bg-opacity-50 rounded-md py-2 px-2 w-[90%] md:w-full h-auto md:h-[440px] flex flex-col">
          <div className="flex flex-row justify-center items-center mt-1 space-x-5">
          <button
              onClick={() => handleButtonClick('album')}
              className={`py-2 px-4 rounded ${activeButton === 'album' ? 'bg-gradient-to-r from-gray-800 to-gray-500 text-white' : 'bg-gradient-to-r from-customBlue1 to-customBlue2 text-white'}`}
            >
              Album
            </button>
            <button
              onClick={() => handleButtonClick('music')}
              className={`py-2 px-4 rounded ${activeButton === 'music' ? 'bg-gradient-to-r from-gray-800 to-gray-500 text-white' : 'bg-gradient-to-r from-customBlue1 to-customBlue2 text-white'}`}
            >
              Music
            </button>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mt-8 flex-grow">
            {/* tambahin loading, waktu eksekusi, dan persentase kemiripan */}
            {currentItems.length > 0 ? (
              currentItems.map((item, index) => (
                activeButton === 'album' ? (
                  <AlbumCard
                    key={index}
                    image={item.image}
                    name={item.name}
                  />
                ) : (
                  <MusicCard
                    key={index}
                    image={item.image}
                    name={item.name}
                    audioSrc={item.audioSrc}
                  />
                )
              ))
            ) : (
              <p></p>
            )}
          </div>
          {currentItems.length > 0 && (
            <div className="flex flex-col items-center mt-2">
              <div className="flex justify-center space-x-4 items-center">
                <button
                  onClick={handlePreviousPage}
                  disabled={currentPage === 1}
                  className="px-4 py-1 bg-gradient-to-r from-customBlue1 to-customBlue2 rounded disabled:opacity-30 hover:bg-white"
                >
                  <span className='text-lg'>&#129168;</span>
                </button>
                <p className="text-white text-[10px]">
                  Page {currentPage} of {totalPages}
                </p>
                <button
                  onClick={handleNextPage}
                  disabled={currentPage === totalPages}
                  className="px-4 py-1 bg-gradient-to-r from-customBlue1 to-customBlue2 rounded disabled:opacity-30 hover:bg-white"
                >
                  <span className='text-lg'>&#129170;</span>
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Album;