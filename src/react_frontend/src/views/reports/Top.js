import React, { useState, useEffect, useRef } from 'react'
import PropTypes from 'prop-types'
import ApiService from '../../services/ApiService'
import { getStyle } from '@coreui/utils'
import { CRow, CCol, CCard, CCardBody, CCardHeader } from '@coreui/react'
import { CChartBar } from '@coreui/react-chartjs'
import { CIcon } from '@coreui/icons-react'
import { cilVideo } from '@coreui/icons'
import PostDetailsOffcanvas from './PostDetailsOffcanvas'

const Top = ({ params }) => {
  const [topPosts, setTopPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [offcanvasVisible, setOffcanvasVisible] = useState(false)
  const [selectedPost, setSelectedPost] = useState(null)
  // Create a ref to store the latest topPosts
  const topPostsRef = useRef([])

  useEffect(() => {
    ApiService.getTopPosts(params)
      .then((response) => {
        setTopPosts(response.data)
        setLoading(false)
      })
      .catch((error) => {
        console.log(error)
        setLoading(false)
      })
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
    console.log(activePoints)
    console.log(topPosts)
    if (activePoints.length > 0) {
      const dataIndex = activePoints[0].index
      const post = topPostsRef.current[dataIndex]

      if (post) {
        setSelectedPost(post)
        setOffcanvasVisible(true)
      }
    }
  }

  // Prepare chart data
  const chartData = {
    labels: topPosts.map((post) => post.description.slice(0, 20)),
    datasets: [
      {
        label: 'Most Views',
        backgroundColor: `rgba(${getStyle('--cui-info-rgb')}, .7)`,
        borderColor: getStyle('--cui-info'),
        data: topPosts.map((post) => post.max_play_count),
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
          text: 'Views',
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
            const post = topPosts[tooltipItem.dataIndex]
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
          <CCardHeader>
            <h4>
              <CIcon icon={cilVideo} size="lg" /> Top Posts by Views
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

Top.propTypes = {
  params: PropTypes.object.isRequired,
}

export default Top
