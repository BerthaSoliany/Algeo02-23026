import React, { useRef, useEffect } from 'react';
import { FaPlayCircle } from 'react-icons/fa';
import MIDI from 'midi.js';

interface MusicCardProps {
  image: string;
  name: string;
  audioSrc?: string; // Make audioSrc optional
}

function MusicCard({ image, name, audioSrc }: MusicCardProps) {
  const audioRef = useRef<HTMLAudioElement>(null);

  useEffect(() => {
    if (audioSrc && audioSrc.endsWith('.mid')) {
      MIDI.loadPlugin({
        soundfontUrl: './soundfont/',
        instrument: 'acoustic_grand_piano',
        onprogress: (state, progress) => {
          console.log(state, progress);
        },
        onsuccess: () => {
          console.log('MIDI plugin loaded');
        },
      });
    }
  }, [audioSrc]);

  const handlePlayPause = () => {
    if (audioSrc && audioSrc.endsWith('.mid')) {
      MIDI.Player.loadFile(audioSrc, MIDI.Player.start);
    } else if (audioRef.current) {
      if (audioRef.current.paused) {
        audioRef.current.play();
      } else {
        audioRef.current.pause();
      }
    }
  };

  return (
    <div className="flex flex-col space-y-1 items-center">
      <div className="w-[160px] h-[100px] p-2 bg-gray-800 rounded-md flex items-center justify-center">
        <img src={image} className="w-full h-full object-contain" alt={name} />
      </div>
      <div className="flex flex-row items-center space-x-1">
        <p className="text-white text-[11px] truncate overflow-hidden text-ellipsis whitespace-nowrap w-[145px]">{name}</p>
        <button onClick={handlePlayPause}>
          <FaPlayCircle className="w-4 h-4 text-white" />
        </button>
        {audioSrc && !audioSrc.endsWith('.mid') && (
          <audio ref={audioRef} src={audioSrc} />
        )}
      </div>
    </div>
  );
}

export default MusicCard;