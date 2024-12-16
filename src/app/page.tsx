import Card from "../components/Card";
import NavBar from "../components/NavBar";

export default function Home() {
  return (
    <div className="relative bg-[url('/image1.png')] bg-cover bg-center p-2 md:p-4 font-custom">
      <div className="flex flex-col items-center justify-center space-y-20">
        <NavBar />
        <div className="bg-black bg-opacity-50 py-10 px-5 rounded-3xl font-bold text-center max-w-[90%] md:max-w-[1000px] space-y-10">
          <h1 className="text-white text-3xl">Selamat datang di <br/>Ikan dan Pisang!</h1>
          <p className="text-white text-md">Ikan dan Pisang adalah program sederhana yang memungkinkan untuk melakukan pencarian gambar album dan lagu berdasarkan database.</p>
          <p className="text-white text-sm">dibuat oleh<br/> tim ikan dan pisang</p>
        </div>
        <div className="bg-black bg-opacity-50 py-10 px-5 rounded-3xl text-center max-w-[90%] md:max-w-[1000px] space-y-5">
          <h1 className="font-bold text-white text-4xl">Cara Menggunakan</h1>
          <div className="flex flex-col md:flex-row justify-center md:space-x-4">
            <Card 
              title="Cari Album" 
              description1="1. Pergi ke menu Finder"
              description2="2. Upload album yang ingin dicari"
              description3="3. Upload dataset yang ingin digunakan"
              description4="4. Klik tombol 'Process AIR' dan tunggu sejenak"
              description5="5. Pilih 'album' atau 'music' untuk menampilkan hasil pencarian"
            />
            <Card 
              title="Cari Lagu" 
              description1="1. Pergi ke menu Finder"
              description2="2. Upload lagu yang ingin dicari"
              description3="3. Upload dataset yang ingin digunakan"
              description4="4. Klik tombol 'process MIR' dan tunggu sejenak"
	      description5="5. Pilih 'album' atau 'music' untuk menampilkan hasil pencarian"
            />
          </div>
        </div>
        <div className="bg-black bg-opacity-50 py-10 px-5 rounded-3xl text-center max-w-[90%] md:max-w-[1000px] space-y-10">
          <h1 className="font-bold text-white text-4xl">Tentang Proyek Ini</h1>
          <p className="text-white text-sm">Ikan dan Pisang adalah program sederhana yang memungkinkan anda untuk melakukan pencarian gambar album dan lagu berdasarkan dataset.</p>
          <p className="text-white text-sm">Terdapat dua fungsi besar yang membuat pencarian album dan lagu dapat dilakukan, yaitu Music Information Retrival (MIR) dan Album Information Retrival (AIR).
          Terdapat pula mapper yang menghubungkan album dan lagu sehingga pencarian album dapat menampilkan lagu dengan album yang sama dan pencarian lagu mempunyai gambar album yang sesuai.</p>
          <p className="text-white text-sm">Pada proyek ini, untuk backend kami menggunakan Python dan Flask. Sedangkan untuk frontend kami menggunakan Next.js, Tailwind CSS, dan TypeScript.</p>
        </div>
      </div>
    </div>
  );
}