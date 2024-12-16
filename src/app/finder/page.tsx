"use client";
import Button from '@/src/components/Button';
import AlbumCard from '@/src/components/AlbumCard';
import MusicCard from '@/src/components/MusicCard';
import NavBar from '@/src/components/NavBar';
import React, { useState, useEffect } from 'react';
import { GoTriangleRight } from "react-icons/go";
import { GoTriangleLeft } from "react-icons/go";
import { ClipLoader } from 'react-spinners';

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
  const [albumData, setAlbumData] = useState<any[]>([]);
  const [musicData, setMusicData] = useState<Music[]>([]);
  const [activeAudio, setActiveAudio] = useState<string | null>(null);
  const itemsPerPage = 15;

  const handlePlayAudio = (audioName: string) => {
    console.log('Setting active audio:', audioName);
    setActiveAudio(audioName); // Hanya satu audio aktif dalam satu waktu
  };  

  const handleButtonClick = (button: 'album' | 'music') => {
    setActiveButton(button);
    setCurrentPage(1);
    setLoading(true);
    setExecutionTime(null);
  };

  const fetchDatasetAudio = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/get-dataset-audio');
        const data = await response.json();

        if (data.success) {
            const audioResults = data.data.map((item: any) => ({
                image: 'default_image_path.png', // Placeholder for audio (can be replaced with actual mapper data if available)
                name: item.name,
                audioSrc: item.audioSrc,
                similarity: 0, // No similarity for plain dataset display
            }));

            setMusicData(audioResults);
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Error fetching dataset audio:', error);
    }
};

  const fetchDatasetImages = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/get-dataset-images');
        const data = await response.json();

        if (data.success) {
            const imageResults = data.data.map((item: any) => ({
                image: item.image,  // URL gambar dari backend
                name: item.name,
                similarity: 0, // No similarity for plain dataset display
            }));

            console.log("Fetched image results:", imageResults); // Debug log
            setAlbumData(imageResults);
        } else {
            alert(`Error: ${data.error}`);
        }
    } catch (error) {
        console.error('Error fetching dataset images:', error);
    }
  };

  // Call fetch functions after uploading dataset
  const uploadDataset = async (file: File) => {
      const formData = new FormData();
      formData.append('file', file);

      try {
          const response = await fetch('http://127.0.0.1:5000/upload-dataset', {
              method: 'POST',
              body: formData,
          });

          if (!response.ok) {
              const errorText = await response.text();
              console.error('Backend error response:', errorText);
              throw new Error(`HTTP error! Status: ${response.status}`);
          }

          const data = await response.json();
          alert(`Dataset uploaded successfully! Extracted folder: ${data.extracted_folder}`);

          // Fetch dataset content
          await fetchDatasetAudio(); // Fetch and display audio dataset
      } catch (error) {
          console.error('Failed to upload dataset:', error);
          alert('Failed to upload dataset.');
      }
  };

  const uploadDatasetImage = async (file: File) => {
      const formData = new FormData();
      formData.append('file', file);

      try {
          const response = await fetch('http://127.0.0.1:5000/upload-dataset-image', {
              method: 'POST',
              body: formData,
          });

          if (!response.ok) {
              const errorText = await response.text();
              console.error('Backend error response:', errorText);
              throw new Error(`HTTP error! Status: ${response.status}`);
          }

          const data = await response.json();
          alert(`Image dataset uploaded successfully! Extracted folder: ${data.extracted_folder}`);

          // Fetch dataset content
          await fetchDatasetImages(); // Fetch and display image dataset
      } catch (error) {
          console.error('Failed to upload image dataset:', error);
          alert('Failed to upload image dataset.');
      }
  };

  const uploadQueryFile = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://127.0.0.1:5000/upload-query', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Backend error response:', errorText);
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Query file uploaded successfully:', data);
        alert(`Query file uploaded successfully! File path: ${data.file_path}`);
    } catch (error) {
        console.error('Failed to upload query file:', error);
        alert('Failed to upload query file.');
    }
};

  const fetchMirResults = async () => {
    const startTime = performance.now();
    try {
        setLoading(true);
        const response = await fetch('http://127.0.0.1:5000/process-similarity', { method: 'POST' });
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        const data = await response.json();

        if (data.success) {
            const mappedResults: Music[] = data.results.map((result: any) => ({
                image: result.image || 'default_image_path.png', // Gambar dari hasil mapper
                name: result.file_name,
                audioSrc: result.audioSrc, // Path audio file
                similarity: result.similarity,
            }));

            setMusicData(mappedResults);
        } else {
            alert(`Error: ${data.error}`);
        }
        setLoading(false);
        const endTime = performance.now();
        const elapsedTime = (endTime - startTime)/1000;
        setExecutionTime(elapsedTime);
    } catch (error) {
        console.error('Failed to fetch similarity results:', error);
        setLoading(false);
    }
  };

  const fetchImageSimilarityResults = async () => {
    const startTime = performance.now();
    try {
      setLoading(true);
      const response = await fetch('http://127.0.0.1:5000/process-image-similarity', { method: 'POST' });
      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
  
      const data = await response.json();
      if (data.success) {
        const mappedResults = data.results.map((result: any) => ({
          image: `http://127.0.0.1:5000/extracted_datasets_image/${result.image_path}`, // URL lengkap gambar
          name: result.file_name, // Nama file untuk ditampilkan
          similarity: result.similarity, // Similarity
        }));
  
        setAlbumData(mappedResults);
      } else {
        alert(`Error: ${data.error}`);
      }
      setLoading(false);
      const endTime = performance.now();
      const elapsedTime = (endTime - startTime)/1000;
      setExecutionTime(elapsedTime);
    } catch (error) {
      console.error('Failed to fetch image similarity results:', error);
      setLoading(false);
    }
  };  

  // replace this with the real time data fetching
  useEffect(() => {
    const fetchData = async () => {
      if (activeButton) {
        // const startTime = performance.now(); // Start time measurement
        try {
          let data;
          if (activeButton === 'album') {
            // Fetch album data
            const response = await fetch('http://127.0.0.1:5000/api/albums'); // Replace with your API endpoint
            data = await response.json();
            setAlbumData(data);
          } else if (activeButton === 'music') {
            // Fetch music data
            const response = await fetch('http://127.0.0.1:5000/api/albums'); // Replace with your API endpoint
            data = await response.json();
            setMusicData(data);
          }
        } catch (error) {
          console.error('Error fetching data:', error);
        } finally {
          // const endTime = performance.now(); // End time measurement
          // setExecutionTime(endTime - startTime); // Calculate execution time
          setLoading(false);
        }
      }
    };

    fetchData();
  }, [activeButton]);

  const handleFileChange = (file: File | null, type: 'upload' | 'datasetAudio' | 'datasetImage' | 'mapper' | 'query') => {
    if (file) {
        const fileName = file.name;
        const fileExtension = fileName.split('.').pop()?.toLowerCase();
        if (type === 'query') {
            uploadQueryFile(file);
        } else if (type === 'upload') {
            setUploadedFileName(file.name);
            if (file.type.startsWith('image/')) {
                const url = URL.createObjectURL(file);
                setUploadedImageUrl(url);
            } else {
                setUploadedImageUrl(null);
            }
        } else if (type === 'datasetAudio') {
            setDatasetAudioFileName(file.name);
            uploadDataset(file);
        } else if (type === 'datasetImage') {
            setDatasetImageFileName(file.name);
            uploadDatasetImage(file);
        } else if (type === 'mapper') {
          uploadMapper(file);
          setMapperFileName(file.name);
        }
    }
};

  const uploadMapper = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:5000/upload-mapper', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Backend error response:', errorText);
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Mapper uploaded successfully:', data);
      alert(`Mapper uploaded successfully! File path: ${data.file_path}`);
    } catch (error) {
      console.error('Failed to upload mapper:', error);
      alert('Failed to upload mapper.');
    }
  };

  const currentData =
  activeButton === 'album'
    ? albumData
    : activeButton === 'music'
    ? musicData
    : [];
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
        <div className="mt-2 bg-black bg-opacity-50 rounded-md py-2 px-2 w-[90%] md:max-w-[320px] min-h-screen flex flex-col justify-center items-center space-y-2">
          {/* search dgn click album/music */}
          {/* mapper dibuat sendiri */}
          <div className="flex flex-col items-center space-y-2">
            {/* Tampilkan pratinjau gambar dan nama file di atas tombol */}
            {uploadedFileName && (
              <div className="flex flex-col items-center space-y-2">
                {/* Jika file adalah gambar, tampilkan pratinjau */}
                {uploadedFileName.match(/\.(jpg|jpeg|png|gif)$/i) && uploadedImageUrl && (
                  <div className="w-[240px] h-[140px] p-2 bg-gray-800 rounded-md flex items-center justify-center">
                    <img
                      src={uploadedImageUrl} // URL objek lokal untuk menampilkan gambar
                      alt="Uploaded Preview"
                      className="w-full h-full object-contain"
                    />
                  </div>
                )}
                {/* Selalu tampilkan nama file */}
                <p className="text-white text-[11px] truncate overflow-hidden text-ellipsis whitespace-nowrap w-[300px] text-center">
                  {uploadedFileName}
                </p>
              </div>
            )}
            {/* Tombol Upload */}
            <Button
              text="Upload"
              onFileChange={(file) => {
                if (file) {
                  handleFileChange(file, 'query'); // Kirim file ke backend menggunakan fungsi yang sudah ada
                  setUploadedFileName(file.name); // Simpan nama file ke state
                  if (file.type.startsWith('image/')) {
                    // Jika file adalah gambar, buat URL untuk pratinjau
                    const url = URL.createObjectURL(file);
                    setUploadedImageUrl(url);
                  } else {
                    // Jika bukan gambar, kosongkan URL gambar
                    setUploadedImageUrl(null);
                  }
                }
              }}
            />
          </div>
          <div className="flex flex-col items-center space-y-2">
            <Button
              text="Dataset Audio"
              onFileChange={(file) => handleFileChange(file, 'datasetAudio')}
            />
            {datasetAudioFileName && (
              <p className="text-white text-[11px] truncate overflow-hidden text-ellipsis whitespace-nowrap w-[300px] text-center">
                Audio: {datasetAudioFileName}
              </p>
            )}
          </div>
          <div className="flex flex-col items-center space-y-2">
            <Button
              text="Dataset Image"
              onFileChange={(file) => handleFileChange(file, 'datasetImage')}
            />
            {datasetImageFileName && (
              <p className="text-white text-[11px] truncate overflow-hidden text-ellipsis whitespace-nowrap w-[300px] text-center">
                Image Dataset: {datasetImageFileName}
              </p>
            )}
          </div>
          <div className="flex flex-col items-center space-y-2">
            <Button
              text="Upload Mapper"
              onFileChange={(file) => handleFileChange(file, 'mapper')}
            />
            {mapperFileName && (
              <p className="text-white text-[11px] truncate overflow-hidden text-ellipsis whitespace-nowrap w-[300px] text-center">
                Mapper: {mapperFileName}
              </p>
            )}
          </div>
          <div className="flex flex-col items-center space-y-2">
            <Button
              text="Process MIR"
              onClick={fetchMirResults}
            />
          </div>
          <div className="flex flex-col items-center space-y-2">
            <Button
              text="Process AIR"
              onClick={fetchImageSimilarityResults}
            />
          </div>
        </div>
        <div className="mt-2 bg-black bg-opacity-50 rounded-md py-2 px-2 w-[90%] md:w-full min-h-screen flex flex-col items-center justify-center">
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
              <ClipLoader color="#ffffff" size={50} />
            </div>
          ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mt-8 flex-grow">
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
                    image={item.image}
                    name={item.name}
                    audioSrc={item.audioSrc}
                    similarity={item.similarity}
                    onPlay={() => handlePlayAudio(item.name)}
                    isPlaying={activeAudio === item.name}
                  />
                )
              ))
            ) : (
              <p>No data available</p>
            )}
          </div>
          )}
          {!loading && executionTime !== null && (
            <p className='text-white text-sm'>Waktu eksekusi: {executionTime.toFixed(2)} s</p>
          )}
          {currentItems.length > 0 && (
            <div className="flex flex-col items-center mt-2">
              <div className="mt-2 text-white text-sm">
                <p>{`${currentItems.length} of ${currentData.length} data`}</p>
              </div>
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