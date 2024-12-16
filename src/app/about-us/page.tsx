import NavBar from '@/src/components/NavBar';
import Profile from '@/src/components/Profile';
import React from 'react'

function AboutUs() {
  return (
    <div className="bg-[url('/image1.png')] bg-cover bg-center min-h-screen flex flex-col p-2 md:p-4 font-custom space-y-10 items-center">
      <NavBar />
      <p className="font-bold text-white text-5xl text-center mt-6">About Us</p>
      <Profile 
        image1='/eiji.png'
        image2="/bertha.jpg"
        name="Bertha Soliany Frandi"
        nim="13523026"
        quote="mau turu tapi belum kelar :<"
      />
      <Profile 
        image1='/drug.png'
        image2="/max.jpg"
        name="Rafen Max Alessandro"
        nim="13523031"
        quote="makasih pondok indah kost udah mau menampung kami tiap malam"
      />
      <Profile 
        image1='/ash.png'
        image2="/grace.jpg"
        name="Grace Evelyn Simon"
        nim="13523087"
        quote="stress is temporary, IPK is forever"
      />
    </div>
  );
}

export default AboutUs;