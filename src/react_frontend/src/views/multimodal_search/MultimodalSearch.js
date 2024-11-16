import React, { useState } from 'react'
import {
  CCard,
  CCardBody,
  CCardHeader,
  CRow,
  CCol,
  CButton,
  CSpinner,
  CTooltip,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilSearch, cilImage, cilX } from '@coreui/icons'

const MultimodalSearch = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedImage, setSelectedImage] = useState(null)
  const [previewUrl, setPreviewUrl] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [searchResults, setSearchResults] = useState([])
  const [error, setError] = useState('')

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

  const handleSearch = async () => {
    if (!searchQuery && !selectedImage) {
      setError('Please enter a search query or select an image')
      return
    }

    setIsLoading(true)
    setError('')

    try {
      const formData = new FormData()
      if (searchQuery) {
        formData.append('query', searchQuery)
      }
      if (selectedImage) {
        formData.append('image', selectedImage)
      }

      const response = await fetch('/search/multimodal', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Search failed')
      }

      const results = await response.json()
      setSearchResults(results)
    } catch (err) {
      setError('Failed to perform search. Please try again.')
      console.error('Search error:', err)
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
              <CButton color="primary" onClick={handleSearch} disabled={isLoading}>
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

        {error && (
          <div className="alert alert-danger" role="alert">
            {error}
          </div>
        )}

        <CRow>
          {searchResults.map((result) => (
            <CCol
              key={`${result.post_id}-${result.element_id}`}
              xs={12}
              md={6}
              lg={4}
              className="mb-4"
            >
              <CCard>
                <img
                  src={`/api/keyframes/${result.post_id}/${result.element_id}`}
                  alt="Key frame"
                  className="card-img-top"
                />
                <CCardBody>
                  <p className="text-muted mb-1">
                    Similarity: {(result.similarity * 100).toFixed(1)}%
                  </p>
                  <p className="mb-2">{result.description}</p>
                  <small className="text-muted">By {result.author.username}</small>
                </CCardBody>
              </CCard>
            </CCol>
          ))}
        </CRow>
      </CCardBody>
    </CCard>
  )
}

export default MultimodalSearch
