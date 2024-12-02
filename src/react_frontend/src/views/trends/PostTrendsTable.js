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
import CIcon from '@coreui/icons-react'
import { cilLink } from '@coreui/icons'

const PostTrendsTable = () => {
  const [trends, setTrends] = useState([])

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        const response = await fetch('http://localhost:80/post-trends')
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
    <CTable align="middle" className="mb-0 border" hover responsive>
      <CTableHead className="text-nowrap">
        <CTableRow>
          <CTableHeaderCell className="bg-body-tertiary">Author</CTableHeaderCell>
          <CTableHeaderCell className="bg-body-tertiary">Description</CTableHeaderCell>
          <CTableHeaderCell className="bg-body-tertiary">Video</CTableHeaderCell>
          <CTableHeaderCell className="bg-body-tertiary">Current Views</CTableHeaderCell>
          <CTableHeaderCell className="bg-body-tertiary">Daily Growth</CTableHeaderCell>
          <CTableHeaderCell className="bg-body-tertiary">Weekly Growth</CTableHeaderCell>
          <CTableHeaderCell className="bg-body-tertiary">Monthly Growth</CTableHeaderCell>
          <CTableHeaderCell className="bg-body-tertiary">Last Updated</CTableHeaderCell>
        </CTableRow>
      </CTableHead>
      <CTableBody>
        {trends.map((trend, index) => {
          const tiktokUrl = `https://www.tiktok.com/@${trend.author_name}/video/${trend.post_id}`
          return (
            <CTableRow key={index}>
              <CTableDataCell>
                <div className="fw-semibold">{trend.author_name}</div>
              </CTableDataCell>
              <CTableDataCell>
                <div className="text-truncate" style={{ maxWidth: '200px' }}>
                  {trend.post_description}
                </div>
              </CTableDataCell>
              <CTableDataCell>
                <a href={tiktokUrl} target="_blank" rel="noopener noreferrer">
                  <CIcon icon={cilLink} className="me-2" />
                  Watch
                </a>
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
          )
        })}
      </CTableBody>
    </CTable>
  )
}

export default PostTrendsTable
