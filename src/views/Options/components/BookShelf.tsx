import React, { useState, useEffect } from 'react'
import axios from 'axios';
import styled from 'styled-components';
import { ResponsiveCirclePackingCanvas } from '@nivo/circle-packing'
import sample from './sample.json'

const Container = styled.div`
  height: 700px;
`

export const BookShelf = () => {
  const [ zoomedId, setZoomedId ] = useState<string | null>(null)
  const [ loading, setLoading ] = useState(false)
  const [ data, setData ] = useState([{
    "title": "ultrices mattis odio donec vitae nisi",
    "classify_DDC": 132.174,
  }])

  useEffect(() => {
    axios
      .get("/mockData/")
      .then((res) => {
        setData(res.data)
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

  // const data = {
  //   "name": 'data',
  //   "value": 0,
  //   "children": [
  //     {
  //       "name": 'literature',
  //       "value": 1,
  //       "children": [{
  //         "name": "Book Title",
  //         "loc": 1
  //       }]
  //     },
  //     {
  //       "name": 'history',
  //       "value": 1,
  //       "children": [{
  //         "name": "Book Title",
  //         "loc": 1
  //       }]
  //     },
  //     {
  //       "name": 'rest',
  //       "value": 1,
  //       "children": [{
  //         "name": "Book Title",
  //         "loc": 1
  //       }]
  //     }
  //   ]
  // }
  
  // books.forEach(book => 
  //   {
  //     if (book.classify_DDC > 800 && book.classify_DDC < 900) {
  //         data.children[0].children.push({
  //           "name": book.title,
  //           "loc": 1
  //         })
  //     } else if (book.classify_DDC > 900 && book.classify_DDC < 1000) {
  //         data.children[1].children.push({
  //           "name": book.title,
  //           "loc": 1
  //         })
  //     } else {
  //         data.children[2].children.push({
  //           "name": book.title,
  //           "loc": 1
  //         })
  //     }
  //   }
  // )

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
      <ResponsiveCirclePackingCanvas
        data={sample[0]}
        margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
        id="name"
        value="loc"
        colors={{ scheme: 'nivo' }}
        childColor={{ from: 'color', modifiers: [ [ 'brighter', 0.4 ] ] }}
        padding={4}
        borderWidth={1}
        borderColor={{ from: 'color', modifiers: [ [ 'darker', 0.5 ] ] }}
        zoomedId={zoomedId}
        motionConfig="slow"
        onClick={node => {
          setZoomedId(zoomedId === node.id ? null : node.id)
        }}
      />
    </Container>
    
  );
}