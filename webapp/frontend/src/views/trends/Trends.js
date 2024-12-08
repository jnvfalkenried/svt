import React from 'react'
import { CCard, CCardHeader, CCardBody } from '@coreui/react'
import PostTrendsTable from './PostTrendsTable'

const Trends = () => {
  return (
    <>
      <CCard className="mb-4">
        <CCardHeader>Post Growth Trends</CCardHeader>
        <CCardBody>
          <PostTrendsTable />
        </CCardBody>
      </CCard>
    </>
  )
}

export default Trends
