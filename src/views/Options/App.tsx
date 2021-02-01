import React, { useState, useEffect } from 'react'
import axios from 'axios';
import { books } from './books';
import styled from 'styled-components';

const BookShelf = styled.div`
  background-color: tan;
`

const Row = styled.div`
  border-bottom: 1px solid #000;
`

export const App = () => {

  const [ shelf, setShelf ] = useState([])
  const [ value, setValue ] = useState('')
  const [ results, setResults ] = useState()

  // useEffect goes here to fetch books on shelf from database
  // useEffect(() => {
  //   db.ref('/').on('value', (querySnapShot:any) => {
  //     let data = querySnapShot.val() ? querySnapShot.val() : {};
  //     let allData = {...data};
  //     setShelf(allData)
  //   });
  // }, [])

  const getBooks = () => {
    let arr = value.replace(/\s+/g, '%20')
    const getBook:{} = {
      url: 'http://classify.oclc.org/classify2/Classify?title=' + arr,
      method: 'GET',
      headers: {
        "Access-Control-Allow-Origin": "http://localhost:3000", 
        "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept",
        'Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
      }
    };

    axios(getBook)
      .then(response => {
        console.log(response)
        // setResults(response)
      });
  }

  return (
    <div>
      {shelf.length === 0 && 
        <h1>You don't seem to have any books! Add some below now.</h1>
      }
      <input 
        value={value} 
        placeholder='Search any book' 
        type="text" 
        onChange={event => setValue(event.target.value)} 
      />
      <button 
        type='submit' 
        onClick={getBooks}>
        Search
      </button>
      {results}
      <BookShelf>
        <Row className='800'>
          <h2>Class 800 - Literature</h2>
          {books.filter((i) => i.dewey > 800 && i.dewey < 900).map((book) =>
            <div>
              <p className="tags">{book.title}</p>
              <p className="timeline">{book.dewey}</p>
            </div>
          )}
          {/* {console.log(books.reduce((a) => (a.dewey < 800), 0))} */}
        </Row>
        <Row className='900'>
          <h2>Class 900 - History & geography</h2>
          {books.filter((i) => i.dewey > 900 && i.dewey < 1000).map((book) =>
            <div>
              <p className="tags">{book.title}</p>
              <p className="timeline">{book.dewey}</p>
            </div>
          )}
        </Row>
      </BookShelf>
    </div>
  );
}