import React from 'react';

type Props = {
  heading: string;
  books: [{
    "title": "ultrices mattis odio donec vitae nisi",
    "classify_DDC": 132.174,
  }]
}

export const Row = ({ heading, books }: Props) => {
  return (
    <div>
      {books.map((book) => 
        <div>
          <p className="tags">{book.title}</p>
          <p className="timeline">{book.classify_DDC}</p>
        </div> 
      )}  
      <h2>{heading}</h2>
    </div>
  );
}