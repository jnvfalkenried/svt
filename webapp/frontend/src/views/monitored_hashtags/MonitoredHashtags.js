import React, { useState, useEffect } from 'react'
import CIcon from '@coreui/icons-react'
import { cilChartPie, cilGraph, cilDataTransferDown } from '@coreui/icons'
import { Link } from 'react-router-dom'
import {
  CCard,
  CCardBody,
  CCardHeader,
  CRow,
  CCol,
  CButton,
  CSpinner,
  CTooltip,
  CInputGroup,
  CFormInput,
  CAlert,
  CPagination,
  CPaginationItem,
  CBadge,
} from '@coreui/react'
import PropTypes from 'prop-types'
import ApiService from '../../services/ApiService'

const API_BASE_URL = '/api'

// PropTypes definitions
const RelatedHashtagPropType = PropTypes.shape({
  id: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
})

const HashtagPropType = PropTypes.shape({
  id: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  daily: PropTypes.number.isRequired,
  weekly: PropTypes.number.isRequired,
  monthly: PropTypes.number.isRequired,
  related: PropTypes.arrayOf(RelatedHashtagPropType).isRequired,
})

const GrowthIndicator = ({ value, period }) => {
  const isPositive = value > 0
  return (
    <div
      className={`d-flex align-items-center justify-content-center ${
        isPositive ? 'text-success' : 'text-danger'
      }`}
    >
      <CIcon icon={isPositive ? cilGraph : cilDataTransferDown} size="sm" className="me-1" />
      <CTooltip content={`${period} growth`}>
        <span>{Math.abs(value).toFixed(1)}%</span>
      </CTooltip>
    </div>
  )
}

GrowthIndicator.propTypes = {
  value: PropTypes.number.isRequired,
  period: PropTypes.string.isRequired,
}

const HashtagSearch = ({ onHashtagAdded }) => {
  const [hashtag, setHashtag] = useState('')
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
    try {
      const response = await ApiService.addHashtag(hashtag.toLowerCase())
      setResponseMessage(response.data.message)
      setHashtag('')
      if (onHashtagAdded) {
        onHashtagAdded()
      }
    } catch (error) {
      console.error('Request failed:', error)
      setResponseMessage('Request failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
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
  )
}

HashtagSearch.propTypes = {
  onHashtagAdded: PropTypes.func,
}

const HashtagCard = ({ tag, onRemove }) => {
  const [isRemoving, setIsRemoving] = useState(false)

  const handleRemove = async () => {
    setIsRemoving(true)
    try {
      await onRemove(tag.id)
    } catch (error) {
      console.error('Error removing hashtag:', error)
    } finally {
      setIsRemoving(false)
    }
  }

  return (
    <CCard className="border-0 shadow-lg hover:shadow-xl transition-shadow duration-200 mb-4">
      <CCardBody className="p-4">
        {/* Header */}
        <div className="d-flex justify-content-between align-items-center mb-4">
          <div className="d-flex align-items-center">
            <h4 className="mb-0">#{tag.title}</h4>
          </div>
          <CButton
            color="danger"
            variant="ghost"
            size="sm"
            onClick={handleRemove}
            disabled={isRemoving}
          >
            {isRemoving ? (
              <>
                <CSpinner size="sm" className="me-2" />
                Removing...
              </>
            ) : (
              'Remove'
            )}
          </CButton>
        </div>

        {/* Action Button */}
        <div className="d-flex justify-content-center my-2">
          <Link to={`/monitored_hashtags/${tag.title}/trending`}>
            <CButton color="primary">View trending posts</CButton>
          </Link>
        </div>

        {/* Related Tags */}
        {tag.related.length > 0 && (
          <div>
            <small className="text-medium-emphasis d-block mb-2">
              Related Hashtags
            </small>
            <div className="d-flex flex-wrap gap-2">
              {tag.related.map((related) => (
                <Link 
                  key={related.id}
                  to={`/monitored_hashtags/${related.title}`}
                  className="text-decoration-none"
                >
                  <CBadge 
                    color="light" 
                    className="px-3 py-2 text-primary hover:bg-primary hover:text-white transition-colors duration-200"
                    shape="rounded-pill"
                  >
                    #{related.title}
                  </CBadge>
                </Link>
              ))}
            </div>
          </div>
        )}
      </CCardBody>
    </CCard>
  )
}

HashtagCard.propTypes = {
  tag: HashtagPropType.isRequired,
  onRemove: PropTypes.func.isRequired,
}

const MonitoredHashtags = () => {
  const [hashtags, setHashtags] = useState([])
  const [loading, setLoading] = useState(true)
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 5 // Show 5 hashtag cards per page

  useEffect(() => {
    fetchHashtags()
  }, [])

  const fetchHashtags = async () => {
    try {
      // First fetch the active hashtags
      const hashtagsResponse = await fetch(`${API_BASE_URL}/hashtags`)
      const hashtagsData = await hashtagsResponse.json()
      const activeHashtags = hashtagsData.filter((tag) => tag.active)

      // Then fetch the growth data from your new endpoint
      const trendsResponse = await fetch(`${API_BASE_URL}/hashtag-trends`)
      const trendsData = await trendsResponse.json()

      // Merge hashtag data with growth data
      const hashtagsWithGrowth = activeHashtags.map((tag) => {
        const trendData = trendsData.items.find((trend) => trend.hashtag_id === tag.id) || {
          daily_growth: 0,
          weekly_growth: 0,
          monthly_growth: 0,
        }
        return {
          ...tag,
          daily: trendData.daily_growth,
          weekly: trendData.weekly_growth,
          monthly: trendData.monthly_growth,
          related: [],
        }
      })

      setHashtags(hashtagsWithGrowth)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching hashtags:', error)
      setLoading(false)
    }
  }

  const removeHashtag = async (id) => {
    try {
      const response = await fetch(`${API_BASE_URL}/hashtags/${id}/deactivate`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (!response.ok) {
        throw new Error('Failed to remove hashtag')
      }

      setHashtags(hashtags.filter((tag) => tag.id !== id))
      // If we remove the last item on the current page, go to the previous page
      const totalPages = Math.ceil((hashtags.length - 1) / itemsPerPage)
      if (currentPage > totalPages && currentPage > 1) {
        setCurrentPage(totalPages)
      }
    } catch (error) {
      console.error('Error removing hashtag:', error)
      throw error
    }
  }

  // Pagination calculations
  const totalPages = Math.ceil(hashtags.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  const currentHashtags = hashtags.slice(startIndex, endIndex)

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center min-vh-50">
        <CSpinner />
      </div>
    )
  }

  return (
    <CRow className="justify-content-center">
      <CCol md={8}>
        <CAlert color="info" className="mb-3">
           Add hashtags to monitor and explore their results
        </CAlert>
        <HashtagSearch onHashtagAdded={fetchHashtags} />
        <CCard className="mb-4">
          <CCardHeader>
            <h4 className="mb-0">
              <CIcon icon={cilChartPie} className="me-2" />
              Monitored Hashtags
            </h4>
          </CCardHeader>
          <CCardBody>
            {hashtags.length > 0 ? (
              <>
                {currentHashtags.map((tag) => (
                  <HashtagCard key={tag.id} tag={tag} onRemove={removeHashtag} />
                ))}
                {totalPages > 1 && (
                  <div className="d-flex justify-content-center mt-4">
                    <CPagination aria-label="Hashtag navigation">
                      <CPaginationItem
                        aria-label="Previous"
                        disabled={currentPage === 1}
                        onClick={() => setCurrentPage(currentPage - 1)}
                      >
                        <span aria-hidden="true">&laquo;</span>
                      </CPaginationItem>
                      {[...Array(totalPages)].map((_, index) => (
                        <CPaginationItem
                          key={index + 1}
                          active={currentPage === index + 1}
                          onClick={() => setCurrentPage(index + 1)}
                        >
                          {index + 1}
                        </CPaginationItem>
                      ))}
                      <CPaginationItem
                        aria-label="Next"
                        disabled={currentPage === totalPages}
                        onClick={() => setCurrentPage(currentPage + 1)}
                      >
                        <span aria-hidden="true">&raquo;</span>
                      </CPaginationItem>
                    </CPagination>
                  </div>
                )}
              </>
            ) : (
              <div className="text-center text-medium-emphasis py-4">
                No hashtags currently being monitored.
              </div>
            )}
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  )
}

export default MonitoredHashtags
