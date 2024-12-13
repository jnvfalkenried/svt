import React, { useState, useEffect } from 'react'
import {
  CTable,
  CTableBody,
  CTableDataCell,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
  CProgress,
} from '@coreui/react'
import PostDetailsOffcanvas from './PostTrendsDetailsOffcanvas'

const PostTrendsTable = () => {
  const [trends, setTrends] = useState([])
  const [selectedPost, setSelectedPost] = useState(null)
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        const response = await fetch('/api/post-trends')
        const data = await response.json()
        setTrends(data.items)
      } catch (error) {
        console.error('Error fetching trends:', error)
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

  return (
    <>
      <CTable align="middle" className="mb-0 border" hover responsive>
        <CTableHead className="text-nowrap">
          <CTableRow>
            <CTableHeaderCell className="bg-body-tertiary">Hashtags</CTableHeaderCell>
            <CTableHeaderCell className="bg-body-tertiary">Post Info</CTableHeaderCell>
            <CTableHeaderCell className="bg-body-tertiary">Current Views</CTableHeaderCell>
            <CTableHeaderCell className="bg-body-tertiary">Daily Growth</CTableHeaderCell>
            <CTableHeaderCell className="bg-body-tertiary">Weekly Growth</CTableHeaderCell>
            <CTableHeaderCell className="bg-body-tertiary">Monthly Growth</CTableHeaderCell>
            <CTableHeaderCell className="bg-body-tertiary">Last Updated</CTableHeaderCell>
          </CTableRow>
        </CTableHead>
        <CTableBody>
          {trends.map((trend, index) => (
            <CTableRow key={index}>
              <CTableDataCell>
                <div className="d-flex flex-wrap gap-2" style={{ maxWidth: '200px' }}>
                  {trend.challenges.slice(0, 3).map((tag, i) => (
                    <span key={i} className="badge bg-body-tertiary text-medium-emphasis">
                      {tag}
                    </span>
                  ))}
                  {trend.challenges.length > 3 && (
                    <span
                      className="badge bg-secondary"
                      title={trend.challenges.slice(3).join(' ')}
                    >
                      +{trend.challenges.length - 3}
                    </span>
                  )}
                </div>
              </CTableDataCell>
              <CTableDataCell>
                <button
                  className="btn btn-ghost-primary"
                  onClick={() => {
                    setSelectedPost(trend)
                    setVisible(true)
                  }}
                >
                  View Details
                </button>
              </CTableDataCell>
              <CTableDataCell>
                <div className="fw-semibold">{trend.current_views.toLocaleString()}</div>
              </CTableDataCell>
              <CTableDataCell>
                <div className="d-flex justify-content-between">
                  <div className="fw-semibold">{trend.daily_growth_rate.toFixed(2)}%</div>
                  <div className="ms-3">
                    <small className="text-body-secondary">
                      {trend.daily_change.toLocaleString()} views
                    </small>
                  </div>
                </div>
                <CProgress
                  thin
                  color={getProgressColor(trend.daily_growth_rate)}
                  value={Math.min(100, Math.abs(trend.daily_growth_rate))}
                />
              </CTableDataCell>
              <CTableDataCell>
                <div className="d-flex justify-content-between">
                  <div className="fw-semibold">{trend.weekly_growth_rate.toFixed(2)}%</div>
                  <div className="ms-3">
                    <small className="text-body-secondary">
                      {trend.weekly_change.toLocaleString()} views
                    </small>
                  </div>
                </div>
                <CProgress
                  thin
                  color={getProgressColor(trend.weekly_growth_rate)}
                  value={Math.min(100, Math.abs(trend.weekly_growth_rate))}
                />
              </CTableDataCell>
              <CTableDataCell>
                <div className="d-flex justify-content-between">
                  <div className="fw-semibold">{trend.monthly_growth_rate.toFixed(2)}%</div>
                  <div className="ms-3">
                    <small className="text-body-secondary">
                      {trend.monthly_change.toLocaleString()} views
                    </small>
                  </div>
                </div>
                <CProgress
                  thin
                  color={getProgressColor(trend.monthly_growth_rate)}
                  value={Math.min(100, Math.abs(trend.monthly_growth_rate))}
                />
              </CTableDataCell>
              <CTableDataCell>
                <div className="small text-body-secondary">Last updated</div>
                <div className="fw-semibold">{new Date(trend.collected_at).toLocaleString()}</div>
              </CTableDataCell>
            </CTableRow>
          ))}
        </CTableBody>
      </CTable>
      <PostDetailsOffcanvas
        visible={visible}
        onClose={() => setVisible(false)}
        post={selectedPost}
      />
    </>
  )
}

export default PostTrendsTable
