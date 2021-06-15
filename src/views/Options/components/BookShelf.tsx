import React from 'react'
import styled from 'styled-components';

const Shelf = styled.div`
  background-color: tan;
`

const Row = styled.div`
  border-bottom: 1px solid #000;
`
export const Props = {
  sectionTitle: String,
  books: Array
}

export const BookShelf = (Props) => {
  return (
    <Shelf>
      <Row className='800'>
        {books.map((book) => 
          book.classify.dewey > 800 && book.classify.dewey < 900 &&
            <div>
              <p className="tags">{book.title}</p>
              <p className="timeline">{book.classify.dewey}</p>
            </div> 
        )}  
        <h2>Class 800 - Literature</h2>
      </Row>
      <Row className='800'>
        {books.map((book) => 
          book.classify.dewey > 800 && book.classify.dewey < 900 &&
            <div>
              <p className="tags">{book.title}</p>
              <p className="timeline">{book.classify.dewey}</p>
            </div> 
        )}  
        <h2>Class 800 - Literature</h2>
      </Row>
    </Shelf>
  );
}