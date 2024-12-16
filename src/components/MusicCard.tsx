import React, { useRef, useEffect, useState } from 'react';
import { FaPlayCircle } from 'react-icons/fa';
import { FaPauseCircle } from 'react-icons/fa';
import { FaExclamationCircle } from 'react-icons/fa';
import MIDI from 'midi.js';

interface MusicCardProps {
  image: string;
  name: string;
  audioSrc?: string;
  similarity: number;
  onPlay?: () => void;
  isPlaying: boolean;
}

function MusicCard({ image, name, audioSrc, similarity, onPlay, isPlaying }: MusicCardProps) {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [hasError, setHasError] = useState(false);

  const handlePlayPause = () => {
    if (!audioSrc) {
      setHasError(true);
      return;
    }

    if (onPlay) onPlay(); // Beritahu Finder untuk menghentikan kartu lain

    if (audioSrc.endsWith('.mid')) {
      if (isPlaying) {
        MIDI.Player.stop();
      } else {
        MIDI.Player.loadFile(audioSrc, () => MIDI.Player.start());
      }
    } else if (audioRef.current) {
      if (audioRef.current.paused) {
        audioRef.current.play().catch(() => setHasError(true));
      } else {
        audioRef.current.pause();
      }
    }
  };

  return (
    <div className="flex flex-col space-y-1">
      <div className="w-[160px] h-[100px] p-2 bg-gray-800 rounded-md flex items-center justify-center">
        <img src={image} className="w-full h-full object-contain" alt={name} />
      </div>
      <div className="flex flex-row items-center space-x-1">
        <p className="text-white text-[11px] truncate overflow-hidden text-ellipsis whitespace-nowrap w-[145px]">{name}</p>
        <button onClick={handlePlayPause}>
          {isPlaying ? (
            <FaPauseCircle className="w-4 h-4 text-white" />
          ) : (
            <FaPlayCircle className="w-4 h-4 text-white" />
          )}
        </button>
        {audioSrc && !audioSrc.endsWith('.mid') && (
          <audio ref={audioRef} src={audioSrc} />
        )}
      </div>
      <p className="text-white text-[8px] truncate overflow-hidden text-ellipsis whitespace-nowrap w-[145px]">{similarity}%</p>
    </div>
  );
}

export default MusicCard;