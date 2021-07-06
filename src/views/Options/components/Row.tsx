import React from 'react';
import styled from 'styled-components';

const Shelf = styled.div`
  background: burlywood;
  padding: 10px 20px;
  border: 1px solid black;
`

const Book = styled.div`
  border: 1px solid black;
  max-height: 230px;
  display: inline-flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  background: white;
  margin: 0 4px 0 4px;
  padding: 4px 8px;
`

const Class = styled.h2`
  text-align: center;
`

type Props = {
  heading: string;
  books: [{
    "title": "ultrices mattis odio donec vitae nisi",
    "classify_DDC": 132.174,
  }]
}

export const Row = ({ heading, books }: Props) => {
  return (
    <Shelf>
      {books.map((book) => 
        <Book>
          {/* <Title>{book.title}</Title>
          <p>{book.classify_DDC}</p> */}
        </Book> 
      )} 
      <Class>{heading}</Class>
    </Shelf>
  );
}