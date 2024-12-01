import Card from "../components/Card";
import NavBar from "../components/NavBar";

export default function Home() {
  return (
    <div className="bg-[url('/bg.png')] bg-cover bg-center min-h-screen flex flex-col mb-10">
      <NavBar />
      <div className="mt-20 mx-auto bg-gray-800 py-1 px-2 rounded-md font-bold text-center max-w-[90%] md:max-w-[550px]">
        <h1 className="text-yellow-400 text-4xl mt-5">Selamat datang di ...!</h1>
        <p className="text-white mt-5">... adalah program sederhana yang memungkinkan anda untuk melakukan pencarian gambar dan lagu berdasarkan database yang kami miliki.</p>
        <p className="text-white text-sm mt-5 mb-2">dirancang oleh,<br/>ikan dan pisang</p>
      </div>
      <div className="mt-20 mx-auto bg-gray-800 py-1 px-2 rounded-md text-center max-w-[90%] md:max-w-[550px]">
        <h1 className="font-bold text-yellow-400 text-4xl mt-5 mb-2">Cara Menggunakan</h1>
        <div className="flex flex-col md:flex-row justify-center md:space-x-4 mb-3 mr-2 ml-2">
          <Card 
            title="Cari Gambar" 
            description="Pilih menu Album, kemudian pilih gambar yang ingin anda cari."
          />
          <Card 
            title="Cari Lagu" 
            description="Pilih menu Music, kemudian pilih lagu yang ingin anda cari."
          />
        </div>
      </div>
      <div className="mt-20 mx-auto bg-gray-800 py-1 px-2 rounded-md text-center max-w-[90%] md:max-w-[550px]">
        <h1 className="font-bold text-yellow-400 text-4xl mt-5">Tentang Proyek Ini</h1>
        <p className="text-white mt-5 text-lg">... adalah program sederhana yang memungkinkan anda untuk melakukan pencarian gambar dan lagu berdasarkan database yang kami miliki.</p>
        <p className="text-white mt-5 text-lg">Pada proyek ini, untuk backend kami menggunakan Python dan .... Sedangkan untuk frontend kami menggunakan Next.js, Tailwind CSS, dan TypeScript.</p>
      </div>
    </div>
  );
}
