import React from 'react'
import { BookShelf } from './components/BookShelf'

export const App = () => {
  // const [ title, setTitle ] = useState('')
  // const [ author, setAuthor ] = useState('')

  // const getByTitle = () => {
  //   let titleParsed = title.replace(/\s+/g, '%20')
  //   window.open(
  //     'http://classify.oclc.org/classify2/ClassifyDemo?search-title-txt=' + titleParsed + '&startRec=0', 
  //     "_blank"
  //   )
  // }

  // const getByAuthor = () => {
  //   let authorParsed = author.replace(/\s+/g, '%20')
  //   window.open(
  //     'http://classify.oclc.org/classify2/ClassifyDemo?search-author-txt=' + authorParsed + '&startRec=0', 
  //     "_blank"
  //   )
  // }

  return (
    <div>
      {/* <form>
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
      </form> */}

      <BookShelf />
    </div> 
  );
}