import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
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
import PostTrendsDetailsOffcanvas from './PostTrendsDetailsOffcanvas'

const TrendingPosts = () => {
  const [trends, setTrends] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedPost, setSelectedPost] = useState(null)
  const [showOffcanvas, setShowOffcanvas] = useState(false)
  const { hashtag_title } = useParams()

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        setLoading(true)
        setError(null)
        console.log('Fetching trends for hashtag:', hashtag_title)
        
        const response = await fetch(`/api/hashtags/${encodeURIComponent(hashtag_title)}/trends`)
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const data = await response.json()
        console.log('Fetched data:', data)
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

  const getProgressColor = (growth) => {
    if (growth >= 75) return 'success'
    if (growth >= 50) return 'info'
    if (growth >= 25) return 'warning'
    return 'danger'
  }

  const handleRowClick = (post) => {
    setSelectedPost(post)
    setShowOffcanvas(true)
  }

  const renderHashtagCell = (hashtagTitle) => {
    const hashtags = hashtagTitle ? hashtagTitle.split(',').map(tag => tag.trim()) : []
    
    return (
      <div className="d-flex flex-wrap gap-2" style={{ maxWidth: '200px' }}>
        {hashtags.slice(0, 3).map((tag, i) => (
          <span key={i} className="badge bg-body-tertiary text-medium-emphasis">
            {tag}
          </span>
        ))}
        {hashtags.length > 3 && (
          <span 
            className="badge bg-secondary"
            title={hashtags.slice(3).join(' ')}
          >
            +{hashtags.length - 3}
          </span>
        )}
      </div>
    )
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
    <>
      <CTable align="middle" className="mb-0 border" hover responsive>
        <CTableHead className="text-nowrap">
          <CTableRow>
            <CTableHeaderCell className="bg-body-tertiary">Hashtag</CTableHeaderCell>
            <CTableHeaderCell className="bg-body-tertiary">Author</CTableHeaderCell>
            <CTableHeaderCell className="bg-body-tertiary">Post description</CTableHeaderCell>
            <CTableHeaderCell className="bg-body-tertiary">Views</CTableHeaderCell>
            <CTableHeaderCell className="bg-body-tertiary">Daily Change</CTableHeaderCell>
            <CTableHeaderCell className="bg-body-tertiary">Weekly Change</CTableHeaderCell>
            <CTableHeaderCell className="bg-body-tertiary">Monthly Change</CTableHeaderCell>
            <CTableHeaderCell className="bg-body-tertiary">Last Updated</CTableHeaderCell>
          </CTableRow>
        </CTableHead>
        <CTableBody>
          {trends.map((trend, index) => (
            <CTableRow
              key={index}
              onClick={() => handleRowClick(trend)}
              style={{ cursor: 'pointer' }}
            >
              <CTableDataCell>
                {renderHashtagCell(trend.hashtag_title)}
              </CTableDataCell>
              <CTableDataCell>{trend.author_nickname}</CTableDataCell>
              <CTableDataCell>{trend.post_description}</CTableDataCell>
              <CTableDataCell>{trend.current_views.toLocaleString()}</CTableDataCell>
              <CTableDataCell>
                <div className="d-flex justify-content-between">
                  <div className="fw-semibold">{trend.daily_change.toLocaleString()}</div>
                </div>
                <CProgress
                  thin
                  color={getProgressColor(trend.daily_growth_rate)}
                  value={Math.min(100, Math.abs(trend.daily_growth_rate * 100))}
                />
              </CTableDataCell>
              <CTableDataCell>
                <div className="d-flex justify-content-between">
                  <div className="fw-semibold">{trend.weekly_change.toLocaleString()}</div>
                </div>
                <CProgress
                  thin
                  color={getProgressColor(trend.weekly_growth_rate)}
                  value={Math.min(100, Math.abs(trend.weekly_growth_rate * 100))}
                />
              </CTableDataCell>
              <CTableDataCell>
                <div className="d-flex justify-content-between">
                  <div className="fw-semibold">{trend.monthly_change.toLocaleString()}</div>
                </div>
                <CProgress
                  thin
                  color={getProgressColor(trend.monthly_growth_rate)}
                  value={Math.min(100, Math.abs(trend.monthly_growth_rate * 100))}
                />
              </CTableDataCell>
              <CTableDataCell>{new Date(trend.collected_at).toLocaleDateString()}</CTableDataCell>
            </CTableRow>
          ))}
        </CTableBody>
      </CTable>

      <PostTrendsDetailsOffcanvas
        visible={showOffcanvas}
        onClose={() => setShowOffcanvas(false)}
        post={{
          ...selectedPost,
          challenges: selectedPost ? [selectedPost.hashtag_title] : [],
          author_name: selectedPost?.author_nickname || 'N/A',
          post_description: selectedPost?.post_description || 'N/A',
        }}
      />
    </>
  )
}

export default TrendingPosts
