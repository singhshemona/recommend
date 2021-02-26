import React, { useState, useEffect } from 'react'
import { books } from './books';
import styled from 'styled-components';
import axios from "axios";

const BookShelf = styled.div`
  background-color: tan;
`

const Row = styled.div`
  border-bottom: 1px solid #000;
`

export const App = () => {

  const [ shelf, setShelf ] = useState([])
  const [ results, setResults ] = useState()

  const [ title, setTitle ] = useState('')
  const [ author, setAuthor ] = useState('')

  // useEffect goes here to fetch books on shelf from database
  useEffect(() => {
    axios
      .get("/api/books/")
      .then((res) => console.log(res.data))
      .catch((err) => console.log(err));
  }, [])

  const getByTitle = () => {
    let titleParsed = title.replace(/\s+/g, '%20')
    window.open(
      'http://classify.oclc.org/classify2/ClassifyDemo?search-title-txt=' + titleParsed + '&startRec=0', 
      "_blank"
    )
  }

  const getByAuthor = () => {
    let authorParsed = author.replace(/\s+/g, '%20')
    window.open(
      'http://classify.oclc.org/classify2/ClassifyDemo?search-author-txt=' + authorParsed + '&startRec=0', 
      "_blank"
    )
  }
   
  return (
    <div>
      {shelf.length === 0 && 
        <h1>You don't seem to have any books! Add some below now.</h1>
      }
      <form>
        <input 
          value={title} 
          placeholder='Search by title' 
          type="text" 
          onChange={event => setTitle(event.target.value)} 
        />
        <button 
          type='submit' 
          onClick={getByTitle}>
          Search by title
        </button>
        <input 
          value={author} 
          placeholder='Search by author' 
          type="text" 
          onChange={event => setAuthor(event.target.value)} 
        />
        <button 
          type='submit' 
          onClick={getByAuthor}>
          Search by author
        </button>
      </form>
      
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