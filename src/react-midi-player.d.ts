declare module 'react-midi-player' {
    import * as React from 'react';
  
    interface MidiPlayerProps {
      src: string;
      onPlay?: () => void;
      onPause?: () => void;
      onEnd?: () => void;
    }
  
    export class MidiPlayer extends React.Component<MidiPlayerProps> {}
  }