import React from 'react'
import { CCard, CCardBody, CCardHeader, CRow, CCol } from '@coreui/react'

const MonitoredHashtags = () => (
  <CRow className="justify-content-center">
    <CCol md={6}>
      <CCard className="mb-4">
        <CCardHeader>
          <h4>Monitored Hashtags</h4>
        </CCardHeader>
        <CCardBody>
          <p>Lorem ipsum bla bla</p>
        </CCardBody>
      </CCard>
    </CCol>
  </CRow>
)

export default MonitoredHashtags
