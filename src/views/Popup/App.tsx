import React from 'react'
import styled from 'styled-components'
// import { getDewey } from '../../content'

const Heading = styled.div`
  font-size: 20px;
`;

const LinkToOptions = styled.a`
  font-weight: bold;
  color: black;
`
// const addToShelf = () => {    
//   getDewey()
// }

export const App = () => {
  return (
    <div>
      <Heading>Welcome to Recommend</Heading>
      <LinkToOptions href="options.html" target="_blank">Options</LinkToOptions>
      <button 
        type='submit' 
        onClick={() => console.log('hello?')}
      >
        Add to Shelf
      </button>
    </div>
  );
}