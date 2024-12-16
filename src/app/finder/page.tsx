"use client";
import Button from '@/src/components/Button';
import AlbumCard from '@/src/components/AlbumCard';
import MusicCard from '@/src/components/MusicCard';
import NavBar from '@/src/components/NavBar';
import React, { useState, useEffect, useCallback } from 'react';
import { GoTriangleRight } from "react-icons/go";
import { GoTriangleLeft } from "react-icons/go";
import { ClipLoader } from 'react-spinners';
import { read } from 'node:fs';

interface Album{
  image: string;
  name: string;
  similarity: number;
}

interface Music{
  image: string;
  name: string;
  audioSrc: string;
  similarity: number;
}

function Finder() {
  const [activeButton, setActiveButton] = useState<'album' | 'music' | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [uploadedFileName, setUploadedFileName] = useState<string | null>(null);
  const [datasetAudioFileName, setDatasetAudioFileName] = useState<string | null>(null);
  const [datasetImageFileName, setDatasetImageFileName] = useState<string | null>(null);
  const [mapperFileName, setMapperFileName] = useState<string | null>(null);
  const [uploadedImageUrl, setUploadedImageUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [executionTime, setExecutionTime] = useState<number | null>(null);
  const [albumData, setAlbumData] = useState<Album[]>([]);
  const [musicData, setMusicData] = useState<Music[]>([]);
  const [mapperData, setMapperData] = useState<any[]>([]);
  const itemsPerPage = 15;

  const handleButtonClick = useCallback((button: 'album' | 'music') => {
    if (loading) return;
    setActiveButton(button);
    setCurrentPage(1);
    setLoading(true);
    setExecutionTime(null); // Reset execution time
  }, [loading]);

  useEffect(() => {
    const fetchData = async () => {
      if (activeButton) {
        const startTime = performance.now(); // Start time measurement
        try {
          let data;
          if (activeButton === 'album') {
            // Fetch album data
            const response = await fetch('http://127.0.0.1:5000/api/albums'); // Replace with your API endpoint
            data = await response.json();
            setAlbumData(data);
          } else if (activeButton === 'music') {
            // Fetch music data
            const response = await fetch('http://127.0.0.1:5000/api/music'); // Replace with your API endpoint
            data = await response.json();
            setMusicData(data);
          }
        } catch (error) {
          console.error('Error fetching data:', error);
        } finally {
          const endTime = performance.now(); // End time measurement
          const elapsedTime = (endTime - startTime)/1000;
          setExecutionTime(elapsedTime); // Calculate execution time
          setLoading(false);
        }
      }
    };

    fetchData();
  }, [activeButton]);

  const handleFileChange = (file: File | null, type: 'upload' | 'datasetAudio' | 'datasetImage' | 'mapper') => {
    if (file) {
      if (type === 'upload') {
        setUploadedFileName(file.name);
        // Check if the uploaded file is an image
        if (file.type.startsWith('image/')|| file.name.endsWith('.mid')) {
          const url = URL.createObjectURL(file);
          setUploadedImageUrl(url);
        } else {
          setUploadedImageUrl(null);
          setUploadedFileName(null);
          alert('Please upload an image file');
        }
      } else if (type === 'datasetAudio') {
        if (file.type.startsWith('audio/') || file.name.endsWith('.mid') || file.name.endsWith('.zip')) {
          setDatasetAudioFileName(file.name);
        } else {
          alert('Please upload an audio file');
        }
      } else if (type === 'datasetImage') {
        if (file.type.startsWith('image/') || file.name.endsWith('.zip')) {
          setDatasetImageFileName(file.name);
        } else {
          alert('Please upload an image file');
        }
      } else if (type === 'mapper') {
        if (file.name.endsWith('.json') || file.name.endsWith('.txt')) {
          setMapperFileName(file.name);
          const reader = new FileReader();
          reader.onload = (e) => {
            const mapperData = JSON.parse(e.target?.result as string);
            setMapperData(mapperData);
          };
          reader.readAsText(file);
        } else {
          alert('Please upload a JSON or TXT file');
        }
      }
    }
  };
  
  const handleMakeMapper = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/generate_mapper_recursive', {
        method: 'POST'
      });
      if (!response.ok) {
        throw new Error('Failed to generate mapper');
      }
      const data = await response.json();
      console.log('Mapper:', data.mapper);
  
      // Muat mapper ke state setelah berhasil dibuat
      await handleLoadMapper();
    } catch (error) {
      console.error('Error:', error);
    }
  };
   

  const handleLoadMapper = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/get_mapper'); // Endpoint untuk mendapatkan mapper.json
      if (!response.ok) {
        throw new Error('Failed to fetch mapper');
      }
      const data: Music[] = await response.json();
      setMapperData(data); // Simpan ke state mapperData
    } catch (error) {
      console.error('Error loading mapper:', error);
    }
  };
  

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

  return (
    <div className="relative bg-[url('/image1.png')] bg-cover bg-center min-h-screen flex flex-col p-2 md:p-4 font-custom">
      <NavBar />
      <div className="flex flex-col space-y-2 md:flex-row md:space-x-5 text-xs items-center">
        <div className="mt-2 bg-black bg-opacity-50 rounded-3xl py-2 px-2 w-[90%] md:max-w-[320px] min-h-screen flex flex-col justify-center items-center space-y-2">
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
              text="Dataset Audio"
              onFileChange={(file) => handleFileChange(file, 'datasetAudio')}
            />
            {datasetAudioFileName && <p className="text-white text-[11px] truncate overflow-hidden text-ellipsis whitespace-nowrap w-[300px] text-center">Audio: {datasetAudioFileName}</p>}
          </div>
          <div className='flex flex-col items-center space-y-2'>
            <Button
              text="Dataset Image"
              onFileChange={(file) => handleFileChange(file, 'datasetImage')}
            />
            {datasetImageFileName && <p className="text-white text-[11px] truncate overflow-hidden text-ellipsis whitespace-nowrap w-[300px] text-center">Image: {datasetImageFileName}</p>}
          </div>
          <div className='flex flex-col items-center space-y-2'>
            <Button
              text="Upload Mapper"
              onFileChange={(file) => handleFileChange(file, 'mapper')}
            />
            {mapperFileName && <p className="text-white text-[11px] truncate overflow-hidden text-ellipsis whitespace-nowrap w-[300px] text-center">Mapper: {mapperFileName}</p>}
          </div>
          <Button
            text="Make Mapper"
            onClick={handleMakeMapper}
          />
        </div>
        <div className="mt-2 bg-black bg-opacity-50 rounded-3xl py-2 px-2 w-[90%] md:w-full min-h-screen flex flex-col items-center justify-center">
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
          {loading ? (
            <div className="flex justify-center items-center mt-8 h-full">
              <ClipLoader color="#ffffff" loading={loading} size={50} />
            </div>
          ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mt-4 flex-grow">
            {currentItems.length > 0 ? (
              currentItems.map((item, index) => (
                activeButton === 'album' ? (
                  <AlbumCard
                    key={index}
                    image={item.image}
                    name={item.name}
                    similarity={item.similarity}
                  />
                ) : (
                  <MusicCard
                    key={index}
                    image={item.image}      // Gambar yang diperoleh dari mapper
                    name={item.name}        // Nama dari API
                    audioSrc={'audioSrc' in item ? (item as Music).audioSrc : ''} // Audio file dari API
                    similarity={item.similarity} // Similarity yang diperoleh dari mapper
                  />
                  // <MusicCard
                  //   key={index}
                  //   image={'image' in item ? (item as Music).image : ''}
                  //   name={item.name}
                  //   audioSrc={'audioSrc' in item ? (item as Music).audioSrc : ''}
                  //   similarity={item.similarity}
                  // />
                )
              ))
            ) : (
              <p></p>
              // mapperData.map((mapperItem, index) => (
              //   <MusicCard
              //     key={index}
              //     image={mapperItem.pic_name}
              //     name={`Music ${index + 1}`} // Optional: Buat nama default
              //     audioSrc={mapperItem.audio_file}
              //     similarity={100} // Optional: Tetapkan nilai default
              //   />
              // ))
            )}
          </div>
          )}
          {!loading && executionTime !== null && (
            <p className='text-white text-sm'>Waktu eksekusi: {executionTime.toFixed(2)} s</p>
          )}
          {currentItems.length > 0 && (
            <div className="flex flex-col items-center mt-2">
              <div className="flex justify-center space-x-4 items-center">
                <button
                  onClick={handlePreviousPage}
                  disabled={currentPage === 1}
                  className="px-4 py-1 bg-gradient-to-r from-customBlue1 to-customBlue2 rounded disabled:opacity-30"
                >
                  <GoTriangleLeft className="w-4 h-4 text-white" />
                </button>
                <p className="text-white text-[10px]">
                  Page {currentPage} of {totalPages}
                </p>
                <button
                  onClick={handleNextPage}
                  disabled={currentPage === totalPages}
                  className="px-4 py-1 bg-gradient-to-r from-customBlue1 to-customBlue2 rounded disabled:opacity-30"
                >
                  <GoTriangleRight className="w-4 h-4 text-white" />
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Finder;