import React, { useState, useEffect } from 'react'
import styled from 'styled-components';
import { Row } from './Row';
import axios from 'axios';

const Shelf = styled.div`
  border-bottom: 1px solid #000;
`

export const BookShelf = () => {
  const [ books, setBooks ] = useState([{
    "title": "ultrices mattis odio donec vitae nisi",
    "classify_DDC": 132.174,
  }])

  useEffect(() => {
    axios
      .get("/mockData/")
      .then((res) => setBooks(res.data))
      .catch((err) => console.log(err));
  }, [])

  // define all categories (arrays) then run filter only once and
  // put each into an array via a switch statement
  let literature:any = books.filter((book) => 
    book.classify_DDC > 800 && book.classify_DDC < 900
  )

  let historyAndGeography:any = books.filter((book) => 
  book.classify_DDC > 900 && book.classify_DDC < 1000
)

  return (
    <div>
      <Row 
        books={literature}
        heading={'Class 800 – Literature'}
      />
      <Row 
        books={historyAndGeography}
        heading={'Class 900 – History and geography'}
      />
      {/* <Shelf>
        {books.map((book) => 
          book.classify_DDC > 800 && book.classify_DDC < 900 &&
            <div>
              <p className="tags">{book.title}</p>
              <p className="timeline">{book.classify_DDC}</p>
            </div> 
        )}  
        <h2>Class 800 – Literature</h2>
      </Shelf>
      <Shelf>
        {books.map((book) => 
          book.classify_DDC > 900 && book.classify_DDC < 1000 &&
            <div>
              <p className="tags">{book.title}</p>
              <p className="timeline">{book.classify_DDC}</p>
            </div> 
        )}  
        <h2>Class 900 – History and geography</h2>
      </Shelf> */}
    </div>
  );
}