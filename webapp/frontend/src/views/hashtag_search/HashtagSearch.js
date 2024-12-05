import React, { useState } from 'react'

import {
  CCard,
  CCardBody,
  CCardHeader,
  CButton,
  CInputGroup,
  CFormInput,
  CRow,
  CCol,
  CAlert,
  CSpinner,
} from '@coreui/react'

import ApiService from '../../services/ApiService'

const HashtagSearch = () => {
  const [hashtag, setHashtag] = useState('') // State to store the input hashtag
  const [responseMessage, setResponseMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const handleInputChange = (e) => {
    setHashtag(e.target.value)
  }

  const handleSubmitHashtag = async () => {
    if (!hashtag) {
      setResponseMessage('Please enter a hashtag')
      return
    }

    setLoading(true)

    // Call the ApiService to add a new hashtag
    ApiService.addHashtag(hashtag.toLowerCase())
      .then((response) => {
        setResponseMessage(response.data.message)
        setLoading(false)
        setHashtag('')
      })
      .catch((error) => {
        console.error('Request failed:', error)
        setResponseMessage('Request failed. Please try again.')
        setLoading(false)
        setHashtag('')
      })
  }

  return (
    <CRow className="justify-content-center">
      <CCol md={6}>
        <CCard className="mb-4">
          <CCardHeader>
            <h4>Enter a new Hashtag</h4>
          </CCardHeader>
          <CCardBody>
            <CInputGroup className="mb-3">
              <CFormInput
                placeholder="Type a hashtag (e.g., React)"
                value={hashtag}
                onChange={handleInputChange}
              />
              <CButton
                color="primary"
                onClick={handleSubmitHashtag}
                disabled={loading}
                className="ms-2"
              >
                {loading ? <CSpinner size="sm" /> : 'Submit Hashtag'}
              </CButton>
            </CInputGroup>
            {responseMessage && (
              <CAlert
                color={responseMessage.startsWith('Error') ? 'danger' : 'success'}
                className="mb-3"
              >
                {responseMessage}
              </CAlert>
            )}
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  )
}

export default HashtagSearch
