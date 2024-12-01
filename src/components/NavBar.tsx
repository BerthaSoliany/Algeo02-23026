"use client";

import React, { useState } from 'react';

function NavBar() {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    const toggleMobileMenu = () => {
      setIsMobileMenuOpen(!isMobileMenuOpen);
    };

  return (
    <div className="mt-4 mx-auto bg-gray-800 border-2 border-white py-1 px-2 rounded-full font-bold text-lg text-center max-w-[550px] sticky top-4 flex items-center justify-between z-20">
        <a href="/">
            <img src="/logo.png" alt="logo" className="w-auto h-16 sm:h-20 mx-5" />
        </a>
        <div className="flex-grow hidden md:flex justify-center">
            <a href="/finder" className="hover:underline mx-1 sm:mx-5 text-yellow-400 hover:text-white border-l border-white pl-2 sm:pl-5">Finder</a>
            <a href="/about-us" className="hover:underline mx-1 sm:mx-5 text-yellow-400 hover:text-white border-l border-white pl-2 sm:pl-5">About Us</a>
        </div>
        <div className="md:hidden">
        <button onClick={toggleMobileMenu} className="text-yellow-400 hover:text-white">
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16m-7 6h7"></path>
          </svg>
        </button>
      </div>
      {isMobileMenuOpen && (
        <div className="absolute top-16 left-0 w-full bg-gray-800 border-t border-black md:hidden">
          <a href="/finder" className="block px-4 py-2 text-yellow-400 hover:bg-yellow-400 hover:text-white">Finder</a>
          <a href="/about-us" className="block px-4 py-2 text-yellow-400 hover:bg-yellow-400 hover:text-white">About Us</a>
        </div>
      )}
    </div>
  );
}

export default NavBar
