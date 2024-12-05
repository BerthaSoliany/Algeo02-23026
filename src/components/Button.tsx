import React, { useRef } from 'react';

interface ButtonProps {
    text : string
    onFileChange?: (file: File | null) => void;
}

const Button: React.FC<ButtonProps> = ({text, onFileChange}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleButtonClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (onFileChange && event.target.files) {
      onFileChange(event.target.files[0]);
    }
  };

  return (
    <div>
        <button 
          onClick={handleButtonClick}
          className="bg-gradient-to-r from-customBlue1 to-customBlue2 text-white text-xs font-bold py-2 px-4 w-auto rounded hover:from-customBlue2 hover:to-customBlue1 shadow-xl active:from-gray-700 active:to-gray-400">
            {text}
        </button>
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          onChange={handleFileChange}
        />
    </div>
  );
};

export default Button;