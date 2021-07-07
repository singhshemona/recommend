import React, { useState, useEffect } from 'react'
import axios from 'axios';
import styled from 'styled-components';
import { ResponsiveCirclePacking } from '@nivo/circle-packing'

const Container = styled.div`
  height: 700px;
`

export const BookShelf = () => {
  const [ zoomedId, setZoomedId ] = useState<string | null>(null)
  const [ loading, setLoading ] = useState(false)
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

  // const literature = {
  //   "name": "Literature",
  //   "children": [{
  //     "name": "Book Title",
  //     "loc": 1
  //   }]
  // }

  // const historyAndGeography = {
  //   "name": "History and Geography",
  //   "children": [{
  //     "name": "Book Title",
  //     "loc": 1
  //   }]
  // }

  // const rest = {
  //   "name": "Rest",
  //   "children": [{
  //     "name": "Book Title",
  //     "loc": 1
  //   }]
  // }

  // const data = {
  //   ...literature,
  //   ...historyAndGeography,
  //   ...rest
  // }

  const data = {
    id: 'data',
    value: 0,
    children: [
      {
        id: 'literature',
        value: 1,
        children: [{
          "name": "Book Title",
          "loc": 1
        }]
      },
      {
        id: 'history',
        value: 1,
        children: [{
          "name": "Book Title",
          "loc": 1
        }]
      },
      {
        id: 'rest',
        value: 1,
        children: [{
          "name": "Book Title",
          "loc": 1
        }]
      }
    ]
  }
  
  books.forEach(book => 
    {
      if (book.classify_DDC > 800 && book.classify_DDC < 900) {
          data.children[0].children.push({
            "name": book.title,
            "loc": 1
          })
      } else if (book.classify_DDC > 900 && book.classify_DDC < 1000) {
          data.children[1].children.push({
            "name": book.title,
            "loc": 1
          })
      } else {
          data.children[2].children.push({
            "name": book.title,
            "loc": 1
          })
      }
    }
  )

  return (
    loading ? 
    <p>Loading...</p> 
    // : books.length === 1 ?
    // <p>You don't seem to have any books! Add some below now.</p>
    :
    // <AllBooks>
    //   <Row 
    //     books={literature}
    //     heading={'Class 800 – Literature'}
    //   />
    //   <Row 
    //     books={historyAndGeography}
    //     heading={'Class 900 – History and geography'}
    //   />
    //   <Row 
    //     books={emptyTest}
    //     heading={'Class Empty – Test'}
    //   />
    // </AllBooks>

    // graph MUST be in a parent container of a defined height or else it will not show up
    <Container> 
      <ResponsiveCirclePacking
        data={data}
        margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
        id="name"
        value="loc"
        colors={{ scheme: 'nivo' }}
        childColor={{ from: 'color', modifiers: [ [ 'brighter', 0.4 ] ] }}
        padding={4}
        borderWidth={1}
        borderColor={{ from: 'color', modifiers: [ [ 'darker', 0.5 ] ] }}
        defs={[
            {
                id: 'lines',
                type: 'patternLines',
                background: 'none',
                color: 'inherit',
                rotation: -45,
                lineWidth: 5,
                spacing: 8
            }
        ]}
        zoomedId={zoomedId}
        motionConfig="slow"
        fill={[ { match: { depth: 1 }, id: 'lines' } ]}
        onClick={node => {
          setZoomedId(zoomedId === node.id ? null : node.id)
        }}
      />
    </Container>
    
  );
}