"use client";
import React, { useState, useRef, useEffect } from 'react'
import { FaPlayCircle, FaPauseCircle, FaExclamationCircle } from 'react-icons/fa';
import MIDI from 'midi.js';

interface PlaylistProps {
    title: string;
    albumSrc: string;
    audioSrc: string;
}

function Playlist({ title, albumSrc, audioSrc }: PlaylistProps) {
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
        <div className='mt-5 bg-[#D9D9D9] text-sm font-custom flex px-5 py-8 rounded-2xl h-24 w-[90%] xl:w-[1000px] items-center justify-start space-x-6 content-center'>
            <button onClick={handlePlayPause}>
            {hasError ? (
                <FaExclamationCircle className="w-7 h-7 text-red-500" />
            ) : isPlaying ? (
                <FaPauseCircle className="w-7 h-7 text-black" />
            ) : (
                <FaPlayCircle className="w-7 h-7 text-black" />
            )}
            </button>
            {audioSrc && !audioSrc.endsWith('.mid') && (
            <audio ref={audioRef} src={audioSrc} onError={handleAudioError} />
            )}
            <img src={albumSrc} alt="album" className="w-auto h-20 mx-5 drop-shadow-dark" />
            <p className='text-black'>{title}</p>
        </div>
    );
};

export default Playlist;