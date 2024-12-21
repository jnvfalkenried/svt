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
  CButton,
} from '@coreui/react'
import { cilCloudDownload } from '@coreui/icons'
import CIcon from '@coreui/icons-react'

const AuthorTrendsTable = () => {
  const [trends, setTrends] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        setLoading(true)
        const response = await fetch('/api/author-trends')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data = await response.json()
        setTrends(data.items || [])
        setError(null)
      } catch (error) {
        console.error('Error fetching author trends:', error)
        setError('Failed to load author trends')
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

  const downloadCSV = () => {
    // Prepare CSV headers
    const headers = [
      'Author Nickname',
      'Unique ID',
      'Current Followers',
      'Current Hearts',
      'Daily Growth Rate (%)',
      'Daily Followers Change',
      'Weekly Growth Rate (%)',
      'Weekly Followers Change',
      'Monthly Growth Rate (%)',
      'Monthly Followers Change',
      'Last Updated',
    ]

    // Prepare CSV rows
    const csvData = trends.map((trend) => [
      trend.author_nickname,
      trend.unique_id,
      trend.current_followers || 0,
      trend.current_hearts || 0,
      trend.daily_followers_growth_rate?.toFixed(2) || 0,
      trend.daily_followers_change || 0,
      trend.weekly_followers_growth_rate?.toFixed(2) || 0,
      trend.weekly_followers_change || 0,
      trend.monthly_followers_growth_rate?.toFixed(2) || 0,
      trend.monthly_followers_change || 0,
      trend.collected_at ? new Date(trend.collected_at).toLocaleString() : 'N/A',
    ])

    // Combine headers and rows
    const csvContent = [headers.join(','), ...csvData.map((row) => row.join(','))].join('\n')

    // Create blob and download
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    const url = URL.createObjectURL(blob)
    link.setAttribute('href', url)
    link.setAttribute('download', `author_trends_${new Date().toISOString().split('T')[0]}.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  if (loading) {
    return (
      <div className="d-flex justify-content-center p-4">
        <CSpinner color="primary" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center p-4 text-danger">
        <p>{error}</p>
      </div>
    )
  }

  if (!trends?.length) {
    return (
      <div className="text-center p-4 text-muted">
        <p>No author trends data available.</p>
      </div>
    )
  }

  return (
    <div>
      <div className="d-flex justify-content-end mb-3">
        <CButton color="primary" onClick={downloadCSV} disabled={!trends.length}>
          <CIcon icon={cilCloudDownload} className="me-2" />
          Download CSV
        </CButton>
      </div>
      <CTable align="middle" className="mb-0 border" hover responsive>
        <CTableHead className="text-nowrap">
          <CTableRow>
            <CTableHeaderCell className="bg-body-tertiary">Author</CTableHeaderCell>
            <CTableHeaderCell className="bg-body-tertiary">Current Stats</CTableHeaderCell>
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
                <div className="fw-semibold">{trend.author_nickname}</div>
                <div className="small text-body-secondary">{trend.unique_id}</div>
              </CTableDataCell>
              <CTableDataCell>
                <div className="d-flex flex-column">
                  <div className="fw-semibold">
                    Followers: {trend.current_followers?.toLocaleString() || 0}
                  </div>
                  <small className="text-body-secondary">
                    Hearts: {trend.current_hearts?.toLocaleString() || 0}
                  </small>
                </div>
              </CTableDataCell>
              <CTableDataCell>
                <div className="d-flex justify-content-between">
                  <div className="fw-semibold">
                    {trend.daily_followers_growth_rate?.toFixed(2) || 0}%
                  </div>
                  <div className="ms-3">
                    <small className="text-body-secondary">
                      {trend.daily_followers_change?.toLocaleString() || 0} followers
                    </small>
                  </div>
                </div>
                <CProgress
                  thin
                  color={getProgressColor(trend.daily_followers_growth_rate || 0)}
                  value={Math.min(100, Math.abs(trend.daily_followers_growth_rate || 0))}
                />
              </CTableDataCell>
              <CTableDataCell>
                <div className="d-flex justify-content-between">
                  <div className="fw-semibold">
                    {trend.weekly_followers_growth_rate?.toFixed(2) || 0}%
                  </div>
                  <div className="ms-3">
                    <small className="text-body-secondary">
                      {trend.weekly_followers_change?.toLocaleString() || 0} followers
                    </small>
                  </div>
                </div>
                <CProgress
                  thin
                  color={getProgressColor(trend.weekly_followers_growth_rate || 0)}
                  value={Math.min(100, Math.abs(trend.weekly_followers_growth_rate || 0))}
                />
              </CTableDataCell>
              <CTableDataCell>
                <div className="d-flex justify-content-between">
                  <div className="fw-semibold">
                    {trend.monthly_followers_growth_rate?.toFixed(2) || 0}%
                  </div>
                  <div className="ms-3">
                    <small className="text-body-secondary">
                      {trend.monthly_followers_change?.toLocaleString() || 0} followers
                    </small>
                  </div>
                </div>
                <CProgress
                  thin
                  color={getProgressColor(trend.monthly_followers_growth_rate || 0)}
                  value={Math.min(100, Math.abs(trend.monthly_followers_growth_rate || 0))}
                />
              </CTableDataCell>
              <CTableDataCell>
                <div className="small text-body-secondary">Last updated</div>
                <div className="fw-semibold">
                  {trend.collected_at ? new Date(trend.collected_at).toLocaleString() : 'N/A'}
                </div>
              </CTableDataCell>
            </CTableRow>
          ))}
        </CTableBody>
      </CTable>
    </div>
  )
}

export default AuthorTrendsTable
