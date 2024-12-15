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
}

function MusicCard({ image, name, audioSrc, similarity }: MusicCardProps) {
  const audioRef = useRef<HTMLAudioElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    if (!audioSrc) {
      setHasError(true);
      return;
    }

    if (audioSrc && audioSrc.endsWith('.mid')) {
      MIDI.loadPlugin({
        soundfontUrl: new URL('https://gleitz.github.io/midi-js-soundfonts/FluidR3_GM/'), // Replace with your SoundFont URL
        instrument: 'acoustic_grand_piano',
        onprogress: (state, progress) => {
          console.log('Loading SoundFont:', state, progress);
        },
        onsuccess: () => {
          console.log('MIDI plugin loaded successfully');
          setHasError(false);
        },
      });
    }
  }, [audioSrc]);

  const handlePlayPause = () => {
    if (!audioSrc) {
      setHasError(true);
      return;
    }

    if (audioSrc && audioSrc.endsWith('.mid')) {
      if (isPlaying) {
        MIDI.Player.stop();
        setIsPlaying(false);
      } else {
        MIDI.Player.loadFile(audioSrc, () => {
          console.log('MIDI file loaded:', audioSrc);
          MIDI.Player.start();
          setIsPlaying(true);
        });
      }
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
    <div className="flex flex-col space-y-1">
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
      <p className="text-white text-[8px] truncate overflow-hidden text-ellipsis whitespace-nowrap w-[145px]">{similarity}%</p>
    </div>
  );
}

export default MusicCard;