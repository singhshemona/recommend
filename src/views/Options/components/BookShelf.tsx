import React, { useState, useEffect } from 'react'
import styled from 'styled-components';
import { Row } from './Row';
import axios from 'axios';

const All = styled.div`
  border-bottom: 1px solid #000;
`

export const BookShelf = () => {
  const [ books, setBooks ] = useState([{
    "title": "ultrices mattis odio donec vitae nisi",
    "classify_DDC": 132.174,
  }])
  const [ loading, setLoading ] = useState(true)

  let literature:any = [];
  let historyAndGeography:any = [];
  let rest:any = [];

  useEffect(() => {
    axios
      .get("/mockData/")
      .then((res) => {
        setBooks(res.data)
        setLoading(false)
      })
      .catch((err) => console.log(err));
  }, [])
 

  // let literature:any = books.filter((book) => 
  //   book.classify_DDC > 800 && book.classify_DDC < 900
  // )

  // let historyAndGeography:any = books.filter((book) => 
  // book.classify_DDC > 900 && book.classify_DDC < 1000

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
    <All>
      <Row 
        books={literature}
        heading={'Class 800 – Literature'}
      />
      <Row 
        books={historyAndGeography}
        heading={'Class 900 – History and geography'}
      />
    </All>
  );
}