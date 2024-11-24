import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import {
  CCard,
  CCardBody,
  CCardHeader,
  CRow,
  CCol,
  CSpinner,
  CBreadcrumb,
  CBreadcrumbItem,
  CButton,
  CTable,
  CTableHead,
  CTableRow,
  CTableHeaderCell,
  CTableBody,
  CTableDataCell,
  CAlert,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilArrowLeft } from '@coreui/icons'

const API_BASE_URL = 'http://localhost'

const TrendingPosts = () => {
  const { id } = useParams()
  const [posts, setPosts] = useState([])
  const [hashtag, setHashtag] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Define dummy data for when no posts are found
  const dummyData = [
    {
      id: 1,
      description: 'Fun dance challenge #viral',
      author: 'DanceKing123',
      followers: '1.2M',
      video_growth_daily: '14.5%',
      video_growth_weekly: '23.3%',
      video_growth_monthly: '34.7%',
      videoLink: 'https://example.com/video1',
    },
    {
      id: 2,
      description: 'Cooking tutorial - Easy pasta recipe',
      author: 'ChefMaster',
      followers: '850K',
      video_growth_daily: '14.5%',
      video_growth_weekly: '23.3%',
      video_growth_monthly: '34.7%',
      videoLink: 'https://example.com/video2',
    },
    {
      id: 3,
      description: 'Daily vlog - Adventure time!',
      author: 'TravelBlogger',
      followers: '2.1M',
      video_growth_daily: '14.5%',
      video_growth_weekly: '23.3%',
      video_growth_monthly: '34.7%',
      videoLink: 'https://example.com/video3',
    },
  ]

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError(null)

        // Fetch hashtag details
        const hashtagResponse = await fetch(`${API_BASE_URL}/hashtags/${id}`)
        if (!hashtagResponse.ok) {
          throw new Error('Loading dummy data for demo')
        }
        const hashtagData = await hashtagResponse.json()
        setHashtag(hashtagData)

        // Fetch trending posts
        const postsResponse = await fetch(`${API_BASE_URL}/hashtags/${id}/trending`)
        if (!postsResponse.ok) {
          throw new Error('Failed to fetch trending posts')
        }
        const postsData = await postsResponse.json()
        setPosts(Array.isArray(postsData) ? postsData : [])
      } catch (error) {
        console.error('Error fetching data:', error)
        setError(error.message)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [id])

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center min-vh-50">
        <CSpinner />
      </div>
    )
  }

  return (
    <>
      <CBreadcrumb>
        <CBreadcrumbItem>
          <Link to="/monitored_hashtags">
            <CIcon icon={cilArrowLeft} className="me-2" />
            Back to Monitored Hashtags
          </Link>
        </CBreadcrumbItem>
        <CBreadcrumbItem active>#{hashtag?.title || 'Loading...'}</CBreadcrumbItem>
      </CBreadcrumb>

      <CRow>
        <CCol>
          {error && (
            <CAlert color="danger" className="mb-4">
              {error}
            </CAlert>
          )}
          <CCard className="mb-4">
            <CCardHeader>
              <h4 className="mb-0">
                Trending Posts {hashtag?.title ? `for #${hashtag.title}` : ''}
              </h4>
              <small className="text-muted">
                {error || posts.length === 0 ? 'Loading dummy data for demonstration' : ''}
              </small>
            </CCardHeader>
            <CCardBody>
              <CTable hover>
                <CTableHead>
                  <CTableRow>
                    <CTableHeaderCell scope="col">Post Description</CTableHeaderCell>
                    <CTableHeaderCell scope="col">Author</CTableHeaderCell>
                    <CTableHeaderCell scope="col"># of Followers</CTableHeaderCell>
                    <CTableHeaderCell scope="col">Video Growth Daily</CTableHeaderCell>
                    <CTableHeaderCell scope="col">Video Growth Weekly</CTableHeaderCell>
                    <CTableHeaderCell scope="col">Video Growth Monthly</CTableHeaderCell>
                    <CTableHeaderCell scope="col">Video Link</CTableHeaderCell>
                  </CTableRow>
                </CTableHead>
                <CTableBody>
                  {(posts.length > 0 ? posts : dummyData).map((item) => (
                    <CTableRow key={item.id}>
                      <CTableDataCell>{item.description || item.title}</CTableDataCell>
                      <CTableDataCell>{item.author}</CTableDataCell>
                      <CTableDataCell>{item.followers}</CTableDataCell>
                      <CTableDataCell>{item.video_growth_daily}</CTableDataCell>
                      <CTableDataCell>{item.video_growth_weekly}</CTableDataCell>
                      <CTableDataCell>{item.video_growth_monthly}</CTableDataCell>
                      <CTableDataCell>
                        <a href={item.videoLink} className="text-decoration-none">
                          View Video
                        </a>
                      </CTableDataCell>
                    </CTableRow>
                  ))}
                </CTableBody>
              </CTable>
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </>
  )
}

export default TrendingPosts
