import React, { useState, useEffect } from 'react'
import { CCard, CCardBody, CCardHeader, CRow, CCol, CButton, CSpinner } from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilSearch, cilImage, cilX } from '@coreui/icons'

const MultimodalSearch = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedImage, setSelectedImage] = useState(null)
  const [previewUrl, setPreviewUrl] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [searchResults, setSearchResults] = useState([])
  const [error, setError] = useState('')
  const [isValid, setIsValid] = useState(false)

  const handleImageSelect = (event) => {
    const file = event.target.files[0]
    if (file) {
      setSelectedImage(file)
      setPreviewUrl(URL.createObjectURL(file))
    }
  }

  const clearImage = () => {
    setSelectedImage(null)
    setPreviewUrl('')
  }

  useEffect(() => {
    setIsValid(!!searchQuery || !!selectedImage)
  }, [searchQuery, selectedImage])

  const handleSearch = async () => {
    if (!isValid) {
      setError('Please enter a search query or select an image')
      return
    }

    setIsLoading(true)
    setError('')
    setSearchResults([])

    try {
      const formData = new FormData()

      if (searchQuery && searchQuery.trim()) {
        formData.append('query', searchQuery.trim())
        console.log('Adding query to form:', searchQuery.trim())
      }

      if (selectedImage) {
        formData.append('image', selectedImage)
        console.log('Adding image to form:', selectedImage.name)
      }

      console.log('FormData contents:')
      for (let pair of formData.entries()) {
        console.log(pair[0] + ': ' + pair[1])
      }

      const response = await fetch('http://localhost/search/multimodal', {
        method: 'POST',
        body: formData,
        headers: { Accept: 'application/json' },
        credentials: 'same-origin',
      })

      console.log('Response status:', response.status)

      let data
      const contentType = response.headers.get('content-type')
      if (contentType && contentType.includes('application/json')) {
        data = await response.json()
      } else {
        const text = await response.text()
        console.error('Unexpected response format:', text)
        throw new Error('Unexpected response format from server')
      }

      if (!response.ok) {
        throw new Error(data.detail || 'Search failed')
      }

      console.log('Search results:', data)

      if (Array.isArray(data) && data.length === 0) {
        setError('No results found')
      } else if (!Array.isArray(data)) {
        console.error('Unexpected data format:', data)
        throw new Error('Unexpected response format')
      } else {
        setSearchResults(data)
      }
    } catch (err) {
      console.error('Search error:', err)
      const errorMessage = err.message.includes('{') ? JSON.parse(err.message).detail : err.message
      setError(`Failed to perform search: ${errorMessage}`)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <CCard className="mb-4">
      <CCardHeader>
        <strong>Multimodal Search</strong>
      </CCardHeader>
      <CCardBody>
        <CRow className="mb-4">
          <CCol xs={12} md={8}>
            <div className="d-flex gap-3">
              <input
                type="text"
                className="form-control"
                placeholder="Enter your search query..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <div className="position-relative">
                <input
                  type="file"
                  accept="image/*"
                  className="d-none"
                  id="imageUpload"
                  onChange={handleImageSelect}
                />
                <CButton
                  color="secondary"
                  onClick={() => document.getElementById('imageUpload').click()}
                >
                  <CIcon icon={cilImage} className="me-2" />
                  Upload Image
                </CButton>
              </div>
              <CButton
                color="primary"
                onClick={handleSearch}
                disabled={isLoading || !isValid}
                title={!isValid ? 'Please enter a search query or select an image' : ''}
              >
                {isLoading ? (
                  <CSpinner size="sm" />
                ) : (
                  <>
                    <CIcon icon={cilSearch} className="me-2" />
                    Search
                  </>
                )}
              </CButton>
            </div>
          </CCol>
        </CRow>

        {previewUrl && (
          <CRow className="mb-4">
            <CCol xs={12} md={4}>
              <div className="position-relative">
                <img
                  src={previewUrl}
                  alt="Preview"
                  className="img-fluid rounded"
                  style={{ maxHeight: '200px' }}
                />
                <CButton
                  color="danger"
                  size="sm"
                  className="position-absolute top-0 end-0 m-2"
                  onClick={clearImage}
                >
                  <CIcon icon={cilX} />
                </CButton>
              </div>
            </CCol>
          </CRow>
        )}

        <CRow>
          {isLoading ? (
            <CCol className="text-center">
              <CSpinner />
              <p>Searching...</p>
            </CCol>
          ) : searchResults.length > 0 ? (
            searchResults.map((result) => (
              <CCol
                key={`${result.post_id}-${result.element_id}`}
                xs={12}
                md={6}
                lg={4}
                className="mb-4"
              >
                <CCard>
                  <CCardBody>
                    <p className="text-muted mb-1">Distance: {result.distance.toFixed(3)}</p>
                    <p className="mb-2">{result.description}</p>
                    <small className="text-muted">By {result.author?.username || 'Unknown'}</small>
                  </CCardBody>
                </CCard>
              </CCol>
            ))
          ) : error ? (
            <CCol>
              <div className="alert alert-danger" role="alert">
                {error}
              </div>
            </CCol>
          ) : null}
        </CRow>
      </CCardBody>
    </CCard>
  )
}

export default MultimodalSearch
