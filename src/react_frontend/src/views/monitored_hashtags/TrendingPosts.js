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

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError(null)

        // Fetch hashtag details
        const hashtagResponse = await fetch(`${API_BASE_URL}/hashtags/${id}`)
        if (!hashtagResponse.ok) {
          throw new Error('Failed to fetch hashtag details')
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

  if (error) {
    return (
      <div className="text-center text-danger p-4">
        <h4>Error loading data</h4>
        <p>{error}</p>
        <Link to="/monitored_hashtags">
          <CButton color="primary">Return to Monitored Hashtags</CButton>
        </Link>
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
        <CBreadcrumbItem active>#{hashtag?.title}</CBreadcrumbItem>
      </CBreadcrumb>

      <CRow>
        <CCol>
          <CCard className="mb-4">
            <CCardHeader>
              <h4 className="mb-0">Trending Posts for #{hashtag?.title}</h4>
            </CCardHeader>
            <CCardBody>
              {posts.length > 0 ? (
                posts.map((post) => (
                  <div key={post.id} className="border-bottom p-3">
                    <h5>{post.title}</h5>
                    <p>{post.content}</p>
                    <div className="d-flex gap-3">
                      <small>Likes: {post.likes}</small>
                      <small>Comments: {post.comments}</small>
                      <small>Shares: {post.shares}</small>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center p-4">
                  <p>No trending posts found for this hashtag.</p>
                </div>
              )}
            </CCardBody>
          </CCard>
        </CCol>
      </CRow>
    </>
  )
}

export default TrendingPosts
