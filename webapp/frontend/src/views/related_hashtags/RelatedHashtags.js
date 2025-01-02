import React, { useState, useEffect } from 'react'
import {
  CTable,
  CTableBody,
  CTableDataCell,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
  CSpinner,
  CAlert,
  CFormSelect,
  CFormInput,
} from '@coreui/react'

const RelatedHashtags = () => {
  const [relatedHashtags, setRelatedHashtags] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [sortBy, setSortBy] = useState('')
  const [confidenceFilter, setConfidenceFilter] = useState('')

  useEffect(() => {
    const fetchRelatedHashtags = async () => {
      try {
        setLoading(true)
        setError(null)

        const response = await fetch('/api/related-hashtags')

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const data = await response.json()
        console.log('Fetched Related Hashtags:', data)
        console.log('Fetched Related Hashtags Items:', data.items)
        setRelatedHashtags(data.related_hashtag_rules || [])
      } catch (error) {
        console.error('Error fetching related hashtags:', error)
        setError('Failed to load related hashtags. Please try again later.')
      } finally {
        setLoading(false)
      }
    }

    fetchRelatedHashtags()
  }, [])

  const handleSortChange = (e) => {
    const sortKey = e.target.value
    setSortBy(sortKey)
    if (sortKey) {
      const sortedHashtags = [...relatedHashtags].sort((a, b) => b[sortKey] - a[sortKey])
      setRelatedHashtags(sortedHashtags)
    }
  }

  const handleConfidenceFilterChange = (e) => {
    setConfidenceFilter(e.target.value)
  }

  const filteredHashtags = relatedHashtags.filter((hashtag) => {
    if (confidenceFilter) {
      return hashtag.confidence >= parseFloat(confidenceFilter)
    }
    return true
  })

  if (loading) {
    return (
      <div className="d-flex justify-content-center p-4">
        <CSpinner />
      </div>
    )
  }

  if (error) return <CAlert color="danger">{error}</CAlert>

  if (relatedHashtags.length === 0)
    return <CAlert color="info">No hashtag associations rules available at the moment.</CAlert>

  return (
    <div>
      <div className="mb-3">
        <p>Sort and filter the hashtag associations below:</p>
        <CFormSelect className="mb-2" aria-label="Sort by" onChange={handleSortChange}>
          <option value="">Sort By</option>
          <option value="support">Support Score</option>
          <option value="confidence">Confidence Score</option>
          <option value="lift">Lift Score</option>
        </CFormSelect>

        <CFormInput
          type="number"
          placeholder="Filter by minimum confidence"
          value={confidenceFilter}
          onChange={handleConfidenceFilterChange}
          min={0.3}
          max={1}
          step={0.1}
        />
      </div>

      <CTable align="middle" className="mb-0 border" hover responsive>
        <CTableHead>
          <CTableRow>
            <CTableHeaderCell className="text-center">Hashtag(s)</CTableHeaderCell>
            <CTableHeaderCell className="text-center">Related Hashtag(s)</CTableHeaderCell>
            <CTableHeaderCell className="text-center">Support Score</CTableHeaderCell>
            <CTableHeaderCell className="text-center">Confidence Score</CTableHeaderCell>
            <CTableHeaderCell className="text-center">Lift Score</CTableHeaderCell>
          </CTableRow>
        </CTableHead>
        <CTableBody>
          {filteredHashtags.map((relatedHashtag, index) => (
            <CTableRow key={index}>
              <CTableDataCell>
                <div className="fw-semibold">{relatedHashtag.hashtags.join(' ')}</div>
              </CTableDataCell>
              <CTableDataCell>
                <div className="d-flex justify-content-between">
                  <div className="fw-semibold">{relatedHashtag.related_hashtags.join(' ')}</div>
                </div>
              </CTableDataCell>
              <CTableDataCell>
                <div className="d-flex justify-content-between">
                  <div className="fw-semibold">{relatedHashtag.support.toFixed(4)}</div>
                </div>
              </CTableDataCell>
              <CTableDataCell>
                <div className="d-flex justify-content-between">
                  <div className="fw-semibold">{relatedHashtag.confidence.toFixed(4)}</div>
                </div>
              </CTableDataCell>
              <CTableDataCell>
                <div className="d-flex justify-content-between">
                  <div className="fw-semibold">{relatedHashtag.lift.toFixed(4)}</div>
                </div>
              </CTableDataCell>
            </CTableRow>
          ))}
        </CTableBody>
      </CTable>
    </div>
  )
}

export default RelatedHashtags
