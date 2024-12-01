import NavBar from '@/src/components/NavBar';
import Profile from '@/src/components/Profile';
import React from 'react'

function AboutUs() {
  return (
    <div className="bg-[url('/bg.png')] bg-cover bg-center min-h-screen flex flex-col mb-5">
      <NavBar />
      <p className="font-bold text-black text-6xl text-center mt-6 text-shadow">About Us</p>
      <Profile 
        image1='/ash.png'
        image2="/bertha.jpg"
        name="Bertha Soliany Frandi"
        nim="13523026"
        quote="..."
      />
      <Profile 
        image1='/eiji.png'
        image2="/bertha.jpg"
        name="Rafen Max Allesandro"
        nim="13523031"
        quote="..."
      />
      <Profile 
        image1='/wong.png'
        image2="/grace.jpg"
        name="Grace Evelyn Simon"
        nim="13523087"
        quote="..."
      />
    </div>
  );
}

export default AboutUs;