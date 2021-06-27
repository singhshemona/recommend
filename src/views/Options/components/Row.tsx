import React from 'react';
import styled from 'styled-components';

const Shelf = styled.div`
  display: flex;
  overflow: scroll;
  background: #f9debb;
  padding: 10px 20px;
`

const Book = styled.div`
  border: 1px solid black;
  max-height: 400px;
  display: inline-flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  background: white;
  margin: 0 10px 0 10px;
  padding: 4px 8px;
`

const Class = styled.h2`
  text-align: center;
  background: burlywood;
  margin-top: 0;
  padding-top: 10px;
  padding-bottom: 10px;
  margin-bottom: 36px;
  border: 1px solid black;
`

const Title = styled.p`
  transform: rotate(180deg);
  writing-mode: vertical-rl;
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
            <Title>{book.title}</Title>
            <p>{book.classify_DDC}</p>
          </Book> 
        )} 
      </Shelf>
      <Class>{heading}</Class>
    </>
  );
}