import React from 'react';
import styled from 'styled-components';

const Shelf = styled.div`
  display: flex;
`

const Book = styled.div`
  border: 1px solid black;
`

const Class = styled.h2`
  text-align: center;
  background: burlywood;
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
    <>
      <Shelf>
        {books.map((book) => 
          <Book>
            <p>{book.title}</p>
            <p>{book.classify_DDC}</p>
          </Book> 
        )} 
      </Shelf>
      <Class>{heading}</Class>
    </>
  );
}