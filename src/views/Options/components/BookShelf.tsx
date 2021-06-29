import React, { useState, useEffect } from 'react'
import { Row } from './Row';
import axios from 'axios';
import styled from 'styled-components';

const AllBooks = styled.div`
  max-width: 900px;
  margin: 0 auto;
  border: 1px solid black;
  background: #f9debb;
  border-radius: 16px;
`
export const BookShelf = () => {
  const [ loading, setLoading ] = useState(true)
  const [ books, setBooks ] = useState([{
    "title": "ultrices mattis odio donec vitae nisi",
    "classify_DDC": 132.174,
  }])

  useEffect(() => {
    axios
      .get("/mockData/")
      .then((res) => {
        setBooks(res.data)
        setLoading(false)
      })
      .catch((err) => console.log(err));
  }, [])

  let literature:any = [];
  let historyAndGeography:any = [];
  let rest:any = [];

  books.forEach(book => 
    {
      if (book.classify_DDC > 800 && book.classify_DDC < 900) {
        literature.push(book)
      } else if (book.classify_DDC > 900 && book.classify_DDC < 1000) {
        historyAndGeography.push(book)
      } else {
        rest.push(book)
      }
    }
  )

  return (
    loading ? 
    <p>Loading...</p>
    :
    <AllBooks>
      <Row 
        books={literature}
        heading={'Class 800 – Literature'}
      />
      <Row 
        books={historyAndGeography}
        heading={'Class 900 – History and geography'}
      />
    </AllBooks>
  );
}