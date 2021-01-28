import React from 'react'
import styled from 'styled-components';

const Heading = styled.div`
  font-size: 20px;
`;

const LinkToOptions = styled.a`
  font-weight: bold;
  color: black;
`

export const App = () => {
  return (
    <div>
      <Heading>Welcome to Recommend</Heading>
      <LinkToOptions href="options.html" target="_blank">Options</LinkToOptions>
    </div>
  );
}