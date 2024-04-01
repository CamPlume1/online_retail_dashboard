import React, { useEffect, useState } from 'react';
import '../ImageContainer.css'; // Import CSS file

const ImageComponent = ({ selectedOption }) => {
  const [imageSrc, setImageSrc] = useState('');

  useEffect(() => {
    const fetchImage = async () => {
      try {
        const response = await fetch(`http://localhost:5000/api/test_graphic/${selectedOption}`);
        if (response.ok) {
          const blob = await response.blob();
          const imageUrl = URL.createObjectURL(blob);
          setImageSrc(imageUrl);
        } else {
          console.error('Failed to fetch image:', response.status);
        }
      } catch (error) {
        console.error('Error fetching image:', error);
      }
    };

    fetchImage();

    // Cleanup function to revoke the object URL when the component unmounts
    return () => {
      if (imageSrc) {
        URL.revokeObjectURL(imageSrc);
      }
    };
  }, [selectedOption]);

  return (
    <div>
      {imageSrc ? (
        <img src={imageSrc} alt="Test Graphic" />
      ) : (
        <p>Loading image...</p>
      )}
    </div>
  );
};


const ImageContainer = () => {
  const [selectedOption, setSelectedOption] = useState('');

  const handleOptionChange = (event) => {
    setSelectedOption(event.target.value);
  };

  return (
    <div className="container">
      <div className="header">
        <h1>Graphic Description Here</h1>
      </div>
      <div className="dropdown-menu">
        <select value={selectedOption} onChange={handleOptionChange}>
          <option value="option1">Option 1</option>
          <option value="option2">Option 2</option>
        </select>
      </div>
      <div className="image-grid-comp">
        <ImageComponent selectedOption={selectedOption} />
      </div>
    </div>
  );
};

export default ImageContainer;

