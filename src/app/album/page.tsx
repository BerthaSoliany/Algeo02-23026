"use client";
import NavBar from '@/src/components/NavBar'
import Playlist from '@/src/components/Playlist'
import React , { useEffect, useState } from 'react'
import { ClipLoader } from 'react-spinners';
import { GoChevronLeft, GoChevronRight, GoArrowLeft } from 'react-icons/go';
import { useParams, useLocation } from 'react-router-dom';


interface PlaylistData {
  title: string;
  albumSrc: string;
  audioSrc: string;
}


function Album() {
  const { albumName } = useParams();
  const [playlistData, setPlaylistData] = useState<PlaylistData[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const itemsPerPage = 4;

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/playlist?album=${albumName}`);
        const data = await response.json();
        setPlaylistData(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    if (albumName) {
      fetchData();
    }
  }, [albumName]);

  const totalPages = Math.ceil(playlistData.length / itemsPerPage);

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
  const currentItems = playlistData.slice(indexOfFirstItem, indexOfLastItem);

  return (
    <div className="relative bg-[url('/image1.png')] bg-cover bg-center min-h-screen flex flex-col p-2 md:p-4 font-custom items-center justify-center">
      <NavBar/>
      <div className="mt-2 bg-black bg-opacity-50 rounded-3xl w-[90%] min-h-screen flex flex-col items-center p-0">
        <div className="bg-black bg-opacity-50 rounded-3xl p-20 w-full h-[220px] flex flex-row items-center items-start space-x-10">
          <div className="absolute left-[7%] top-[18%]">
            <a href="/finder">
            <button>
              <GoArrowLeft className="w-7 h-7 text-white"/>
            </button>
            </a>
          </div>
          <img src={`./${albumName}`} alt="Album" className="w-[30%] h-auto md:w-[20%] md:h-auto" />
          <div className="ml-5 flex flex-col space-y-4 truncate overflow-hidden whitespace-nowrap">
            <h1 className="text-white text-lg">Playlist</h1>
            <p className="text-white text-3xl">{albumName}</p>
          </div>
        </div>
        <p className="text-white text-xl mt-5 -ml-[51%]">Songs</p>
        {loading ? (
          <ClipLoader color="#ffffff" loading={loading} size={50} />
        ) : (
          currentItems.map((item, index) => (
            <Playlist
              key={index}
              title={item.title}
              albumSrc={item.albumSrc}
              audioSrc={item.audioSrc}
            />
          ))
        )}
        <div className="flex justify-center space-x-4 items-center mt-4">
          <button
            onClick={handlePreviousPage}
            disabled={currentPage === 1}
            className="disabled:opacity-30 hover:bg-white">
            <GoChevronLeft className="w-10 h-10 text-white" />
          </button>
          <button
            onClick={handleNextPage}
            disabled={currentPage === totalPages}
            className="disabled:opacity-30 hover:bg-white">
            <GoChevronRight className="w-10 h-10 text-white" />
          </button>
        </div>
      </div>
    </div>
  );
}

export default Album;