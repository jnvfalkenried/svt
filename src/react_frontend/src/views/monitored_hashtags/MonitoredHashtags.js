import React, { useState, useEffect } from 'react'
import CIcon from '@coreui/icons-react'
import {
  cilChartPie,
  cilGraph,
  cilLoopCircular,
  cilPencil,
  cilDataTransferDown,
} from '@coreui/icons'
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
import PropTypes from 'prop-types'

const API_BASE_URL = 'http://localhost:80'

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

const HashtagCard = ({ tag }) => (
  <CCard className="mb-4 shadow-sm">
    <CCardBody className="p-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div className="d-flex align-items-center">
          <CIcon icon={cilPencil} size="lg" className="text-primary me-2" />
          <h4 className="mb-0">#{tag.title}</h4>
        </div>
        {/* <CButton color="danger" variant="ghost" size="sm" onClick={() => removeHashtag(tag.id)}> */}
        <CButton color="danger" variant="ghost" size="sm">
          Remove
        </CButton>
      </div>

      <div className="bg-light p-3 rounded mb-4">
        <CRow xs={4} className="text-center">
          <medium className="text-medium-bold d-block mb-4">Posts growth</medium>
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
        <CButton color="primary">View trending posts for hashtag</CButton>
      </div>

      <div>
        <div className="d-flex align-items-center mb-2">
          <CIcon icon={cilLoopCircular} size="sm" className="text-primary me-2" />
          <small className="text-medium-emphasis">Related Hashtags</small>
        </div>
        <div className="d-flex flex-wrap gap-2">
          {tag.related.map((related) => (
            <span key={related.id} className="badge bg-light text-primary rounded-pill">
              #{related.title}
            </span>
          ))}
        </div>
      </div>
    </CCardBody>
  </CCard>
)

HashtagCard.propTypes = {
  tag: HashtagPropType.isRequired,
}

const MonitoredHashtags = () => {
  const [hashtags, setHashtags] = useState([])
  const [loading, setLoading] = useState(true)

  const getGrowthData = (hashtagId) => ({
    daily: Math.random() * 20 - 10,
    weekly: Math.random() * 30 - 15,
    monthly: Math.random() * 40 - 20,
    related: [
      { id: `${hashtagId}-1`, title: 'related1' },
      { id: `${hashtagId}-2`, title: 'related2' },
      { id: `${hashtagId}-3`, title: 'related3' },
    ],
  })

  useEffect(() => {
    fetchHashtags()
  }, [])

  const fetchHashtags = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/hashtags`)
      const data = await response.json()
      const activeHashtags = data
        .filter((tag) => tag.active)
        .map((tag) => ({
          ...tag,
          ...getGrowthData(tag.id),
        }))
      setHashtags(activeHashtags)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching hashtags:', error)
      setLoading(false)
    }
  }

  const removeHashtag = async (id) => {
    try {
      await fetch(`${API_BASE_URL}/hashtags/${id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ active: false }),
      })
      setHashtags(hashtags.filter((tag) => tag.id !== id))
    } catch (error) {
      console.error('Error removing hashtag:', error)
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
        <CCard className="mb-4">
          <CCardHeader>
            <h4 className="mb-0">
              <CIcon icon={cilChartPie} className="me-2" />
              Monitored Hashtags
            </h4>
          </CCardHeader>
          <CCardBody>
            {hashtags.length > 0 ? (
              hashtags.map((tag) => <HashtagCard key={tag.id} tag={tag} />)
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
