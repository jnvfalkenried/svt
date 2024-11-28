import React, { useState, useEffect, useRef } from 'react'
import PropTypes from 'prop-types'
import ApiService from '../../services/ApiService'
import { CRow, CCol, CCard, CCardBody, CCardHeader } from '@coreui/react'
import { CChartBar } from '@coreui/react-chartjs'
import { CIcon } from '@coreui/icons-react'
import { cilVideo } from '@coreui/icons'
import { getStyle } from '@coreui/utils'
import PostDetailsOffcanvas from './PostDetailsOffcanvas'

const Feed = ({ params }) => {
  const [feedPosts, setFeedPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [offcanvasVisible, setOffcanvasVisible] = useState(false)
  const [selectedPost, setSelectedPost] = useState(null)

  // Create a ref to store the latest feedPosts
  const feedPostsRef = useRef([])

  useEffect(() => {
    ApiService.getTopPosts(params)
      .then((response) => {
        setFeedPosts(response.data)
        setLoading(false)
      })
      .catch((error) => {
        console.log(error)
        setLoading(false)
      })
  }, [params])

  useEffect(() => {
    feedPostsRef.current = feedPosts
  }, [feedPosts])

  const handleBarClick = (event) => {
    const activePoints = event.chart.getElementsAtEventForMode(
      event.native,
      'nearest',
      { intersect: true },
      true,
    )
    if (activePoints.length > 0) {
      const dataIndex = activePoints[0].index
      const post = feedPostsRef.current[dataIndex]

      if (post) {
        setSelectedPost(post)
        setOffcanvasVisible(true)
      }
    }
  }

  // Prepare chart data
  const chartData = {
    labels: feedPosts.map((post) => post.description.slice(0, 20)),
    datasets: [
      {
        label: 'Appearances in Feed',
        backgroundColor: `rgba(${getStyle('--cui-info-rgb')}, .7)`,
        borderColor: getStyle('--cui-info'),
        data: feedPosts.map((post) => post.appearances_in_feed),
        hoverBackgroundColor: getStyle('--cui-info'),
        hoverBorderColor: getStyle('--cui-info'),
      },
    ],
  }

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
          text: 'Appearances',
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
            const post = feedPosts[tooltipItem.dataIndex]
            return [
              //`Description: ${post.description}`,
              ` Plays: ${post.max_play_count}`,
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
          <CCardHeader>
            <h4>
              <CIcon icon={cilVideo} size="lg" /> Top Feed Posts
            </h4>
          </CCardHeader>
          <CCardBody>
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

Feed.propTypes = {
  params: PropTypes.object.isRequired,
}

export default Feed
