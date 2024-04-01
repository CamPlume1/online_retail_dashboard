import React from 'react';
import './App.css';
import ImageContainer from "./components/ImageContainer";

function App() {
  return (
     <div className="App">
      <header className="App-header">
        <h1>DS 4300: Retail Analytics App For Small Online Businesses</h1>
      </header>
      <body className="App-body">
        <div className="image-grid">
          <ImageContainer />
          <ImageContainer />
          <ImageContainer />
          <ImageContainer />
        </div>
      </body>
      <footer className="App-footer">
        <p>Created By: Cameron Plume, Nicholas Perrotta, Tom McDonagh, Reece Calvin, and Andrew Enelow</p>
      </footer>
    </div>
  );
}

export default App;
