import Card from "../components/Card";
import NavBar from "../components/NavBar";

export default function Home() {
  return (
    <div className="relative bg-[url('/image1.png')] bg-cover bg-center p-2 md:p-4 font-custom">
      <div className="flex flex-col items-center justify-center space-y-10">
        <NavBar />
        <div className="bg-black bg-opacity-50 py-10 px-5 rounded-3xl font-bold text-center max-w-[90%] md:max-w-[1000px] space-y-10">
          <h1 className="text-white text-4xl">Selamat datang di ...!</h1>
          <p className="text-white text-md">... adalah program sederhana yang memungkinkan untuk melakukan pencarian gambar album dan lagu berdasarkan database.</p>
          <p className="text-white text-sm">dirancang oleh,<br/>ikan dan pisang</p>
        </div>
        <div className="bg-black bg-opacity-50 py-10 px-5 rounded-3xl text-center max-w-[90%] md:max-w-[1000px] space-y-5">
          <h1 className="font-bold text-white text-4xl">Cara Menggunakan</h1>
          <div className="flex flex-col md:flex-row justify-center md:space-x-4">
            <Card 
              title="Cari Album" 
              description="Pergi ke menu Finder, Upload album yang ingin dicari, Upload dataset yang ingin digunakan, Klik tombol 'Album', daftar lagu yang berhubungan dengan album dapat dilihat dengan klik album yang bersangkutan"
            />
            <Card 
              title="Cari Lagu" 
              description="Pergi ke menu Finder, Upload lagu yang ingin dicari, Upload dataset yang ingin digunakan, Klik tombol 'lagu'"
            />
          </div>
        </div>
        <div className="bg-black bg-opacity-50 py-10 px-5 rounded-3xl text-center max-w-[90%] md:max-w-[1000px] space-y-5">
          <h1 className="font-bold text-white text-4xl">Tentang Proyek Ini</h1>
          <p className="text-white text-sm">... adalah program sederhana yang memungkinkan anda untuk melakukan pencarian gambar album dan lagu berdasarkan.</p>
          <p className="text-white text-sm">Pada proyek ini, untuk backend kami menggunakan Python dan Flask. Sedangkan untuk frontend kami menggunakan Next.js, Tailwind CSS, dan TypeScript.</p>
        </div>
      </div>
    </div>
  );
}
