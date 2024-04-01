import React, { useState } from 'react';
import ImageComponent from './ImageComponent';
import '../ImageContainer.css'; // Import CSS file

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
        <ImageComponent customizationData={selectedOption} />
      </div>
    </div>
  );
};

export default ImageContainer;
