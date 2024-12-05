import React from 'react'
import { CCard, CCardBody, CCardHeader, CRow, CCol } from '@coreui/react'

const About = () => (
  <CRow className="justify-content-center">
    <CCol md={6}>
      <CCard className="mb-4">
        <CCardHeader>
          <h4>About</h4>
        </CCardHeader>
        <CCardBody>
          <p>Hashtag monitoring application version 1.0.0</p>
        </CCardBody>
      </CCard>
    </CCol>
  </CRow>
)

export default About
