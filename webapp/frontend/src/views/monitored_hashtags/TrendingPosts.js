import React, { useState, useEffect } from 'react'
import {
  CTable,
  CTableBody,
  CTableDataCell,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
  CProgress,
  CSpinner,
  CAlert,
} from '@coreui/react'

const TrendingPosts = () => {
  const [trends, setTrends] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        setLoading(true)
        setError(null)
        const response = await fetch('/api/hashtag-trends')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data = await response.json()
        setTrends(data.items || [])
      } catch (error) {
        console.error('Error fetching trends:', error)
        setError('Failed to load hashtag trends. Please try again later.')
      } finally {
        setLoading(false)
      }
    }
    fetchTrends()
  }, [])

  const getProgressColor = (growth) => {
    if (growth >= 75) return 'success'
    if (growth >= 50) return 'info'
    if (growth >= 25) return 'warning'
    return 'danger'
  }

  if (loading) {
    return (
      <div className="d-flex justify-content-center p-4">
        <CSpinner />
      </div>
    )
  }

  if (error) return <CAlert color="danger">{error}</CAlert>

  if (!trends.length) return <CAlert color="info">No hashtag trends available at this time.</CAlert>

  return (
    <CTable align="middle" className="mb-0 border" hover responsive>
      <CTableHead className="text-nowrap">
        <CTableRow>
          <CTableHeaderCell className="bg-body-tertiary">Hashtag</CTableHeaderCell>
          <CTableHeaderCell className="bg-body-tertiary">Daily Growth</CTableHeaderCell>
          <CTableHeaderCell className="bg-body-tertiary">Weekly Growth</CTableHeaderCell>
          <CTableHeaderCell className="bg-body-tertiary">Monthly Growth</CTableHeaderCell>
        </CTableRow>
      </CTableHead>
      <CTableBody>
        {trends.map((trend, index) => (
          <CTableRow key={index}>
            <CTableDataCell>
              <div className="fw-semibold">{trend.hashtag_title}</div>
            </CTableDataCell>
            <CTableDataCell>
              <div className="d-flex justify-content-between">
                <div className="fw-semibold">{trend.daily_growth.toFixed(2)}%</div>
              </div>
              <CProgress
                thin
                color={getProgressColor(trend.daily_growth)}
                value={Math.min(100, Math.abs(trend.daily_growth))}
              />
            </CTableDataCell>
            <CTableDataCell>
              <div className="d-flex justify-content-between">
                <div className="fw-semibold">{trend.weekly_growth.toFixed(2)}%</div>
              </div>
              <CProgress
                thin
                color={getProgressColor(trend.weekly_growth)}
                value={Math.min(100, Math.abs(trend.weekly_growth))}
              />
            </CTableDataCell>
            <CTableDataCell>
              <div className="d-flex justify-content-between">
                <div className="fw-semibold">{trend.monthly_growth.toFixed(2)}%</div>
              </div>
              <CProgress
                thin
                color={getProgressColor(trend.monthly_growth)}
                value={Math.min(100, Math.abs(trend.monthly_growth))}
              />
            </CTableDataCell>
          </CTableRow>
        ))}
      </CTableBody>
    </CTable>
  )
}

export default TrendingPosts
