import React, { useState, useEffect } from 'react'
import {
  CTable,
  CTableBody,
  CTableDataCell,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
  CProgress,
  CButton,
  CPagination,
  CPaginationItem,
  CSpinner,
} from '@coreui/react'
import { cilCloudDownload } from '@coreui/icons'
import CIcon from '@coreui/icons-react'
import PostDetailsOffcanvas from './PostTrendsDetailsOffcanvas'

const PostTrendsTable = () => {
  const [trends, setTrends] = useState([])
  const [selectedPost, setSelectedPost] = useState(null)
  const [visible, setVisible] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 10

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        setLoading(true)
        const response = await fetch('/api/post-trends')
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data = await response.json()
        setTrends(data.items || [])
        setError(null)
      } catch (error) {
        console.error('Error fetching trends:', error)
        setError('Failed to load post trends')
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
      'Hashtags',
      'Current Views',
      'Daily Growth Rate (%)',
      'Daily Views Change',
      'Weekly Growth Rate (%)',
      'Weekly Views Change',
      'Monthly Growth Rate (%)',
      'Monthly Views Change',
      'Last Updated',
    ]

    // Prepare CSV rows
    const csvData = trends.map((trend) => [
      trend.challenges.join(', '),
      trend.current_views,
      trend.daily_growth_rate.toFixed(2),
      trend.daily_change,
      trend.weekly_growth_rate.toFixed(2),
      trend.weekly_change,
      trend.monthly_growth_rate.toFixed(2),
      trend.monthly_change,
      new Date(trend.collected_at).toLocaleString(),
    ])

    // Combine headers and rows
    const csvContent = [headers.join(','), ...csvData.map((row) => row.join(','))].join('\n')

    // Create blob and download
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    const url = URL.createObjectURL(blob)
    link.setAttribute('href', url)
    link.setAttribute('download', `post_trends_${new Date().toISOString().split('T')[0]}.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  // Pagination logic
  const totalPages = Math.ceil(trends.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  const currentTrends = trends.slice(startIndex, endIndex)

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
        <p>No post trends data available.</p>
      </div>
    )
  }

  return (
    <div>
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
            <CTableHeaderCell className="bg-body-tertiary text-end">
              <CButton
                color="primary"
                size="sm"
                onClick={downloadCSV}
                disabled={!trends.length}
                className="p-1"
              >
                <CIcon icon={cilCloudDownload} />
              </CButton>
            </CTableHeaderCell>
          </CTableRow>
        </CTableHead>
        <CTableBody>
          {currentTrends.map((trend, index) => (
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
              <CTableDataCell />
            </CTableRow>
          ))}
        </CTableBody>
      </CTable>

      {totalPages > 1 && (
        <div className="d-flex justify-content-end mt-3">
          <CPagination aria-label="Page navigation">
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

      <PostDetailsOffcanvas
        visible={visible}
        onClose={() => setVisible(false)}
        post={selectedPost}
      />
    </div>
  )
}

export default PostTrendsTable
