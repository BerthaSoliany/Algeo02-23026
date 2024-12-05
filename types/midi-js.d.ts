declare module 'midi.js' {
    interface LoadPluginOptions {
      soundfontUrl: URL;
      instrument: string;
      onprogress?: (state: string, progress: number) => void;
      onsuccess?: () => void;
    }
  
    interface Player {
      loadFile: (url: string, callback: () => void) => void;
      start: () => void;
      stop: () => void;
    }
  
    const MIDI: {
      loadPlugin: (options: LoadPluginOptions) => void;
      Player: Player;
    };
  
    export default MIDI;
  }