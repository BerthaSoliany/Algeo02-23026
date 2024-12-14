import React, { useRef, useState } from 'react';
import { FaPlayCircle, FaPauseCircle, FaExclamationCircle } from 'react-icons/fa';
import { MidiPlayer } from 'react-midi-player';

interface MusicCardProps {
  image: string;
  name: string;
  audioSrc?: string;
  similarity: number;
}

function MusicCard({ image, name, audioSrc, similarity }: MusicCardProps) {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [hasError, setHasError] = useState(false);

  const handlePlayPause = () => {
    if (!audioSrc) {
      setHasError(true);
      return;
    }

    if (audioSrc.endsWith('.mid')) {
      setIsPlaying(!isPlaying);
    } else if (audioRef.current) {
      if (audioRef.current.paused) {
        audioRef.current.play().catch((error) => {
          console.error('Error playing audio file:', error);
          setHasError(true);
        });
        setIsPlaying(true);
      } else {
        audioRef.current.pause();
        setIsPlaying(false);
      }
    }
  };

  const handleAudioError = () => {
    console.error('Error loading audio file:', audioSrc);
    setHasError(true);
  };

  return (
    <div className="flex flex-col space-y-1 items-center">
      <div className="w-[160px] h-[100px] p-2 bg-gray-800 rounded-md flex items-center justify-center">
        <img src={image} className="w-full h-full object-contain" alt={name} />
      </div>
      <div className="flex flex-row items-center space-x-1">
        <p className="text-white text-[11px] truncate overflow-hidden text-ellipsis whitespace-nowrap w-[145px]">{name}</p>
        <button onClick={handlePlayPause}>
          {hasError ? (
            <FaExclamationCircle className="w-4 h-4 text-red-500" />
          ) : isPlaying ? (
            <FaPauseCircle className="w-4 h-4 text-white" />
          ) : (
            <FaPlayCircle className="w-4 h-4 text-white" />
          )}
        </button>
        {audioSrc && !audioSrc.endsWith('.mid') && (
          <audio ref={audioRef} src={audioSrc} onError={handleAudioError} />
        )}
      </div>
      {audioSrc && audioSrc.endsWith('.mid') && isPlaying && (
        <MidiPlayer
          src={audioSrc}
          onPlay={() => setIsPlaying(true)}
          onPause={() => setIsPlaying(false)}
          onEnd={() => setIsPlaying(false)}
        />
      )}
      <p className="text-white text-[8px] truncate overflow-hidden text-ellipsis whitespace-nowrap w-[145px]">{similarity}%</p>
    </div>
  );
}

export default MusicCard;