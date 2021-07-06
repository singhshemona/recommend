import React, { useState, useEffect } from 'react'
import { Row } from './Row';
import axios from 'axios';
import styled from 'styled-components';
import { ResponsiveCirclePacking } from '@nivo/circle-packing'

const Container = styled.div`
  height: 700px;
`

export const BookShelf = () => {
  const [ zoomedId, setZoomedId ] = useState<string | null>(null)
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
  
  let emptyTest:any = [];

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

  const data = {
    "name": "Literature",
    "children": [
        {
          "name": "Normal People", // id
          "loc": 1 // value
        },
        {
          "name": "Call Me By Your Name",
          "loc": 1
        },
        {
          "name": "A Thousand Splendid Suns",
          "loc": 1
        },
        {
          "name": "Radical Acceptance",
          "loc": 1
        }
    ]
  }

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
        enableLabels={true}
        labelsFilter={function(e){return 2===e.node.depth}}
        labelsSkipRadius={10}
        labelTextColor={{ from: 'color', modifiers: [ [ 'darker', 2 ] ] }}
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