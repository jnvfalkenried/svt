import React, { useState, useEffect } from 'react'
import CIcon from '@coreui/icons-react'
import { cilChartPie, cilGraph, cilLoopCircular, cilDataTransferDown } from '@coreui/icons'
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
    <CCard className="mb-4 shadow-sm">
      <CCardBody className="p-4">
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

        <div className="bg-body-tertiary p-3 rounded mb-4">
          <CRow>
            <CCol className="text-center mb-3">
              <p className="text-medium-bold mb-0">Posts growth</p>
            </CCol>
          </CRow>
          <CRow>
            <CCol xs={4} className="text-center border-end">
              <small className="text-medium-emphasis d-block mb-2">Daily</small>
              <GrowthIndicator value={tag.daily} period="Daily" />
            </CCol>
            <CCol xs={4} className="text-center border-end">
              <small className="text-medium-emphasis d-block mb-2">Weekly</small>
              <GrowthIndicator value={tag.weekly} period="Weekly" />
            </CCol>
            <CCol xs={4} className="text-center">
              <small className="text-medium-emphasis d-block mb-2">Monthly</small>
              <GrowthIndicator value={tag.monthly} period="Monthly" />
            </CCol>
          </CRow>
        </div>

        <div className="d-flex justify-content-center my-2">
          <Link to={`/monitored_hashtags/${tag.title}/trending`}>
            <CButton color="primary">View trending posts for hashtag</CButton>
          </Link>
        </div>

        <div>
          <div className="d-flex align-items-center mb-2">
            <CIcon icon={cilLoopCircular} size="sm" className="text-primary me-2" />
            <small className="text-medium-emphasis">Related Hashtags</small>
          </div>
          <div className="d-flex flex-wrap gap-2">
            {tag.related.map((related) => (
              <span key={related.id} className="badge bg-body-tertiary text-primary rounded-pill">
                #{related.title}
              </span>
            ))}
          </div>
        </div>
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
      console.log('Trends Data:', trendsData)

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
          related: [], // Will be populated when related hashtags endpoint is available
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
    } catch (error) {
      console.error('Error removing hashtag:', error)
      throw error
    }
  }

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
              hashtags.map((tag) => <HashtagCard key={tag.id} tag={tag} onRemove={removeHashtag} />)
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
