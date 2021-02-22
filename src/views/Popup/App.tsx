import React from 'react'
import styled from 'styled-components';

const Heading = styled.div`
  font-size: 20px;
`;

const LinkToOptions = styled.a`
  font-weight: bold;
  color: black;
`
const addToShelf = () => {    
  console.log('hello?')
  console.log(document.querySelector("#classSummaryData tbody tr:nth-child(1) td:nth-child(2)")!.innerHTML)
}

export const App = () => {
  return (
    <div>
      <Heading>Welcome to Recommend</Heading>
      <LinkToOptions href="options.html" target="_blank">Options</LinkToOptions>
      <button 
        type='submit' 
        onClick={addToShelf}>
        Add to Shelf
      </button>
    </div>
  );
}