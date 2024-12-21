import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import {
  CTable,
  CTableBody,
  CTableDataCell,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
  CSpinner,
  CAlert,
  CButton,
  CPagination,
  CPaginationItem,
} from '@coreui/react'
import { cilCloudDownload } from '@coreui/icons'
import CIcon from '@coreui/icons-react'
import PostTrendsDetailsOffcanvas from './PostTrendsDetailsOffcanvas'

const TrendingPosts = () => {
  const [trends, setTrends] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedPost, setSelectedPost] = useState(null)
  const [showOffcanvas, setShowOffcanvas] = useState(false)
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 10
  const { hashtag_title } = useParams()

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        setLoading(true)
        setError(null)
        const response = await fetch(`/api/hashtags/${encodeURIComponent(hashtag_title)}/trends`)
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data = await response.json()
        setTrends(data || [])
      } catch (error) {
        console.error('Error fetching trends:', error)
        setError(error.message || 'Failed to load hashtag trends')
      } finally {
        setLoading(false)
      }
    }

    if (hashtag_title) {
      fetchTrends()
    }
  }, [hashtag_title])

  const handleRowClick = (post) => {
    setSelectedPost(post)
    setShowOffcanvas(true)
  }

  const downloadCSV = () => {
    // Prepare CSV headers
    const headers = ['Hashtag', 'Author', 'Post Description', 'Views', 'Last Updated']

    // Prepare CSV rows
    const csvData = trends.map((trend) => [
      trend.hashtag_title,
      trend.author_nickname,
      trend.post_description,
      trend.current_views,
      new Date(trend.collected_at).toLocaleDateString(),
    ])

    // Combine headers and rows
    const csvContent = [headers.join(','), ...csvData.map((row) => row.join(','))].join('\n')

    // Create blob and download
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    const url = URL.createObjectURL(blob)
    link.setAttribute('href', url)
    link.setAttribute(
      'download',
      `hashtag_trends_${hashtag_title}_${new Date().toISOString().split('T')[0]}.csv`,
    )
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  const renderHashtagCell = (hashtagTitle) => {
    const hashtags = hashtagTitle ? hashtagTitle.split(',').map((tag) => tag.trim()) : []

    return (
      <div className="d-flex flex-wrap gap-2" style={{ maxWidth: '200px' }}>
        {hashtags.slice(0, 3).map((tag, i) => (
          <span key={i} className="badge bg-body-tertiary text-medium-emphasis">
            {tag}
          </span>
        ))}
        {hashtags.length > 3 && (
          <span className="badge bg-secondary" title={hashtags.slice(3).join(' ')}>
            +{hashtags.length - 3}
          </span>
        )}
      </div>
    )
  }

  // Pagination logic
  const totalPages = Math.ceil(trends.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  const currentTrends = trends.slice(startIndex, endIndex)

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
    <div>
      <CTable align="middle" className="mb-0 border" hover responsive>
        <CTableHead className="text-nowrap">
          <CTableRow>
            <CTableHeaderCell className="bg-body-tertiary" style={{ width: '20%' }}>
              Hashtag
            </CTableHeaderCell>
            <CTableHeaderCell className="bg-body-tertiary" style={{ width: '15%' }}>
              Author
            </CTableHeaderCell>
            <CTableHeaderCell className="bg-body-tertiary" style={{ width: '30%' }}>
              Post description
            </CTableHeaderCell>
            <CTableHeaderCell className="bg-body-tertiary" style={{ width: '15%' }}>
              Views
            </CTableHeaderCell>
            <CTableHeaderCell className="bg-body-tertiary" style={{ width: '15%' }}>
              Last Updated
            </CTableHeaderCell>
            <CTableHeaderCell className="bg-body-tertiary text-end" style={{ width: '5%' }}>
              <CButton
                color="primary"
                size="sm"
                onClick={(e) => {
                  e.stopPropagation()
                  downloadCSV()
                }}
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
            <CTableRow
              key={index}
              onClick={() => handleRowClick(trend)}
              style={{ cursor: 'pointer' }}
            >
              <CTableDataCell>{renderHashtagCell(trend.hashtag_title)}</CTableDataCell>
              <CTableDataCell>{trend.author_nickname}</CTableDataCell>
              <CTableDataCell>
                <div
                  className="text-truncate"
                  style={{ maxWidth: '300px' }}
                  title={trend.post_description}
                >
                  {trend.post_description}
                </div>
              </CTableDataCell>
              <CTableDataCell>{trend.current_views.toLocaleString()}</CTableDataCell>
              <CTableDataCell>{new Date(trend.collected_at).toLocaleDateString()}</CTableDataCell>
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

      <PostTrendsDetailsOffcanvas
        visible={showOffcanvas}
        onClose={() => setShowOffcanvas(false)}
        post={{
          ...selectedPost,
          challenges: selectedPost ? [selectedPost.hashtag_title] : [],
          author_name: selectedPost?.author_nickname || 'N/A',
          post_description: selectedPost?.post_description || 'N/A',
          current_views: selectedPost?.current_views?.toLocaleString() || 'N/A',
          collected_at: selectedPost?.collected_at ? 
            new Date(selectedPost.collected_at).toLocaleDateString() : 'N/A',
        }}
      />
    </div>
  )
}

export default TrendingPosts
