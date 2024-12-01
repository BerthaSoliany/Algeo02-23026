import NavBar from '@/src/components/NavBar';
import React from 'react'

function Album() {
  return (
    <div className="bg-[url('/bg.png')] bg-cover bg-center min-h-screen flex flex-col">
      <NavBar />
      <div className="mt-20 mx-auto bg-gray-800 py-1 px-2 rounded-md font-bold text-lg text-center max-w-[550px]">
        <h1 className="text-yellow-400 text-3xl mt-5">Selamat datang di ...!</h1>
        <p className="text-white mt-5">... adalah program sederhana yang memungkinkan anda untuk melakukan pencarian gambar dan lagu berdasarkan database yang kami miliki.</p>
        <p className="text-white text-sm mt-5 mb-2">dirancang oleh,<br/>ikan dan pisang</p>
      </div>
    </div>
  );
}

export default Album;