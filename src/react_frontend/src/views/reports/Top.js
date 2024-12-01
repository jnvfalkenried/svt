import React, { useState, useEffect, useRef, useMemo } from 'react'
import PropTypes from 'prop-types'
import ApiService from '../../services/ApiService'
import { getStyle } from '@coreui/utils'
import { CRow, CCol, CCard, CCardBody, CButton, CButtonGroup } from '@coreui/react'
import { CChartBar } from '@coreui/react-chartjs'
import { CIcon } from '@coreui/icons-react'
import { cilVideo } from '@coreui/icons'
import PostDetailsOffcanvas from './PostDetailsOffcanvas'

const Top = ({ params }) => {
  const categories = ['Views', 'Likes', 'Comments', 'Shares', 'Saves'] // 'Reposts' is always 0
  const [topPosts, setTopPosts] = useState({})
  const [loading, setLoading] = useState(true)
  const [offcanvasVisible, setOffcanvasVisible] = useState(false)
  const [selectedPost, setSelectedPost] = useState(null)
  const [activeCategory, setActiveCategory] = useState('Views')
  const activePosts = topPosts[activeCategory] || []

  // Create a ref to store the latest topPosts
  const topPostsRef = useRef({})

  useEffect(() => {
    const fetchTopPosts = async () => {
      try {
        const newTopPosts = {}
        for (const el of categories) {
          const response = await ApiService.getTopPosts({ ...params, category: el })
          newTopPosts[el] = response.data
        }
        setTopPosts(newTopPosts)
      } catch (error) {
        console.error(error)
      } finally {
        setLoading(false)
      }
    }

    fetchTopPosts()
  }, [params])

  // Update the ref with the latest topPosts whenever the state changes
  useEffect(() => {
    topPostsRef.current = topPosts
  }, [topPosts])

  const handleBarClick = (event) => {
    const activePoints = event.chart.getElementsAtEventForMode(
      event.native,
      'nearest',
      { intersect: true },
      true,
    )
    if (activePoints.length > 0) {
      const dataIndex = activePoints[0].index
      const post = topPostsRef.current[activeCategory][dataIndex]

      if (post) {
        setSelectedPost(post)
        setOffcanvasVisible(true)
      }
    }
  }

  // Prepare chart data based on the active category
  const chartData = useMemo(
    () => ({
      labels: activePosts.map((post) => post.description.slice(0, 20)),
      datasets: [
        {
          label: activeCategory,
          backgroundColor: `rgba(${getStyle('--cui-info-rgb')}, .7)`,
          borderColor: getStyle('--cui-info'),
          data: activePosts.map((post) => {
            switch (activeCategory) {
              case 'Views':
                return post.max_play_count
              case 'Likes':
                return post.max_digg_count
              case 'Comments':
                return post.max_comment_count
              case 'Shares':
                return post.max_share_count
              case 'Reposts':
                return post.max_repost_count
              case 'Saves':
                return post.max_collect_count
              default:
                return post.max_play_count
            }
          }),
          hoverBackgroundColor: getStyle('--cui-info'),
          hoverBorderColor: getStyle('--cui-info'),
        },
      ],
    }),
    [activePosts, activeCategory],
  )

  // Chart options (you can customize these)
  const chartOptions = {
    responsive: true,
    onClick: handleBarClick,
    scales: {
      x: {
        title: {
          display: true,
          text: 'Posts',
        },
        grid: {
          color: getStyle('--cui-border-color-translucent'),
          drawOnChartArea: false,
        },
        ticks: {
          color: getStyle('--cui-body-color'),
        },
      },
      y: {
        title: {
          display: true,
          text: activeCategory,
        },
        border: {
          color: getStyle('--cui-border-color-translucent'),
        },
        grid: {
          color: getStyle('--cui-border-color-translucent'),
        },
      },
    },
    plugins: {
      tooltip: {
        callbacks: {
          label: function (tooltipItem) {
            const post = activePosts[tooltipItem.dataIndex]
            return [
              //`Description: ${post.description}`,
              //` Plays: ${post.max_play_count}`,
              ` Likes: ${post.max_digg_count}`,
              ` Comments: ${post.max_comment_count}`,
              ` Shares: ${post.max_share_count}`,
              ` Reposts: ${post.max_repost_count}`,
              //`Appearances in Feed: ${post.appearances_in_feed}`,
              //`Created At: ${new Date(post.created_at * 1000).toLocaleString()}`,
            ]
          },
        },
      },
    },
  }

  return (
    <CRow>
      <CCol>
        <CCard>
          <CCardBody>
            <CRow>
              <CCol sm={5}>
                <h4 id="topPosts" className="card-title mb-0">
                  <CIcon icon={cilVideo} size="lg" /> Top Posts by {activeCategory}
                </h4>
              </CCol>
              <CCol sm={7} className="d-none d-md-block">
                <CButtonGroup className="float-end me-3">
                  {categories.map((value) => (
                    <CButton
                      color="outline-secondary"
                      key={value}
                      //className="mx-0"
                      active={activeCategory === value}
                      onClick={() => setActiveCategory(value)}
                    >
                      {value}
                    </CButton>
                  ))}
                </CButtonGroup>
              </CCol>
            </CRow>
            {loading ? (
              <p>Loading posts...</p>
            ) : (
              <div>
                <CChartBar data={chartData} options={chartOptions} />
              </div>
            )}
          </CCardBody>
        </CCard>
      </CCol>
      <PostDetailsOffcanvas
        visible={offcanvasVisible}
        onClose={() => setOffcanvasVisible(false)}
        post={selectedPost}
      />
    </CRow>
  )
}

Top.propTypes = {
  params: PropTypes.object.isRequired,
}

export default Top
