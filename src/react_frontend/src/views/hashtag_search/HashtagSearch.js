import React, { useEffect, useState } from 'react'

import {
  CCard,
  CCardBody,
  CCardHeader,
  CButton,
  CInputGroup,
  CFormInput,
  CRow,
  CCol,
  CListGroup,
  CListGroupItem,
  CAlert,
  CSpinner,
} from '@coreui/react'

const HashtagSearch = () => {
  const [hashtag, setHashtag] = useState('') // State to store the input hashtag
  const [responseMessage, setResponseMessage] = useState('')
  const [activeHashtags, setActiveHashtags] = useState([])
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
    try {
      const response = await fetch('http://localhost:80/hashtag', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ hashtag }), // Send the hashtag as JSON
      })

      if (response.ok) {
        const data = await response.json()
        setResponseMessage(`Success: ${data.message}`)

        // If hashtag is successfully added, update the list of hashtags
        setActiveHashtags((prevHashtags) => [...prevHashtags, { title: hashtag, active: true }])
      } else {
        const errorData = await response.json()
        setResponseMessage(`Error: ${errorData.detail}`)
      }
    } catch (error) {
      console.error('Request failed:', error)
      setResponseMessage('Request failed. Please try again.')
    }
  }

  useEffect(() => {
    // Call the FastAPI hashtag endpoint
    fetch('http://localhost:80/hashtags')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch hashtag')
        }
        return response.json()
      })
      .then((data) => {
        setActiveHashtags(data)
      })
      .catch((error) => {
        console.error('Request failed:', error)
      })
  }, [])

  return (
    <CRow className="justify-content-center">
      <CCol md={6}>
        <CCard className="mb-4">
          <CCardHeader>
            <h4>Multimodal Search</h4>
          </CCardHeader>
          <CCardBody>
            <CInputGroup className="mb-3">
              <CFormInput
                placeholder="Type keywords (e.g. Trump)"
                value={hashtag}
                onChange={handleInputChange}
              />
              <CButton
                color="primary"
                onClick={handleSubmitHashtag}
                disabled={loading}
                className="ms-2"
              >
                {loading ? <CSpinner size="sm" /> : 'Search'}
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
