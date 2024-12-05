import React, { useState } from 'react'
import { CCard, CCardBody, CCardHeader, CRow, CCol, CButton, CSpinner, CBadge } from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilSearch, cilImage, cilX, cilHeart, cilPeople, cilUserFollow } from '@coreui/icons'
import ApiService from '../../services/ApiService'

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

  const formatDate = (timestamp) => {
    if (!timestamp) return 'Unknown date'
    const date = new Date(timestamp * 1000)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  const handleSearch = async () => {
    if (!searchQuery && !selectedImage) {
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
      }

      if (selectedImage) {
        formData.append('image', selectedImage)
      }

      const response = await fetch('http://localhost/search/multimodal', {
        method: 'POST',
        body: formData,
        headers: {
          Accept: 'application/json',
        },
      })

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

  const renderPostInfo = (post, author) => {
    if (!author || !post) return 'Post information is not available'

    const authorUniqueId = author.author_unique_id || 'unknown-author' // Provide a fallback value
    const tiktokUrl = `https://www.tiktok.com/@${authorUniqueId}/video/${post.id || 'unknown-id'}`

    return (
      <div className="post-info">
        <div className="d-flex align-items-center gap-2">
          <strong>Username: {author.nickname || 'Unknown'}</strong>{' '}
        </div>
        <div className="d-flex align-items-center gap-2">
          <small>Signature: {author.signature || 'Unknown'}</small>{' '}
        </div>
        <div className="d-flex gap-3 text-muted small mt-1">
          {author.follower_count !== undefined && (
            <span>
              <CIcon icon="cilUser" size="sm" /> {author.follower_count.toLocaleString()} followers
            </span>
          )}
          {author.following_count !== undefined && (
            <span>
              <CIcon icon="cilArrowRight" size="sm" /> {author.following_count.toLocaleString()}{' '}
              following
            </span>
          )}
          {author.heart_count !== undefined && (
            <span>
              <CIcon icon="cilLike" size="sm" /> {author.heart_count.toLocaleString()} likes
            </span>
          )}
        </div>

        {/* Additional post statistics */}
        <div className="d-flex gap-3 text-muted small mt-1">
          {post.max_digg_count !== 0 && (
            <span>
              <CIcon icon="cilThumbUp" size="sm" /> {post.max_digg_count.toLocaleString()} likes
            </span>
          )}
          {post.max_play_count !== 0 && (
            <span>
              <CIcon icon="cilPlayCircle" size="sm" /> {post.max_play_count.toLocaleString()} views
            </span>
          )}
          {post.max_share_count !== 0 && (
            <span>
              <CIcon icon="cilShareAlt" size="sm" /> {post.max_share_count.toLocaleString()} shares
            </span>
          )}
          {post.max_collect_count !== 0 && (
            <span>
              <CIcon icon="cilBookmark" size="sm" /> {post.max_collect_count.toLocaleString()} saves
            </span>
          )}
        </div>

        <div className="mt-2">
          <a href={tiktokUrl} target="_blank" rel="noopener noreferrer" className="btn btn-primary">
            Watch Post on TikTok
          </a>
        </div>
      </div>
    )
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
                disabled={isLoading || (!searchQuery && !selectedImage)}
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
              <CCol key={`${result.post_id}-${result.element_id}`} xs={12} className="mb-4">
                <CCard>
                  <CCardBody>
                    <div className="d-flex justify-content-between align-items-start mb-3">
                      <div className="flex-grow-1">
                        {renderPostInfo(result.post, result.author)}
                      </div>
                      <div className="text-end ms-3">
                        <p className="text-muted mb-1">Similarity score: {result.similarity}</p>
                        {result.created_at && (
                          <small className="text-muted d-block">
                            Posted: {formatDate(result.created_at)}
                          </small>
                        )}
                      </div>
                    </div>
                    <div className="post-content">
                      {/* <p className="mb-2">Description:</p> */}
                      <p className="mb-2">Description: {result.description}</p>
                      <div className="d-flex gap-2 mt-2 flex-wrap">
                        {result.duet_enabled && (
                          <CBadge color="success" className="px-2">
                            Duet Enabled
                          </CBadge>
                        )}
                        {result.is_ad && (
                          <CBadge color="warning" className="px-2">
                            Advertisement
                          </CBadge>
                        )}
                        {result.can_repost && (
                          <CBadge color="info" className="px-2">
                            Repostable
                          </CBadge>
                        )}
                        {result.music_id && (
                          <CBadge color="dark" className="px-2">
                            Has Music
                          </CBadge>
                        )}
                      </div>
                    </div>
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
