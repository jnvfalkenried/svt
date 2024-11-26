import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import ApiService from '../../services/ApiService'
import { CRow, CCol, CCard, CCardBody, CCardHeader } from '@coreui/react'
import { CChartBar } from '@coreui/react-chartjs'
import { CIcon } from '@coreui/icons-react'
import { cilVideo } from '@coreui/icons'
import { getStyle } from '@coreui/utils'

const Feed = ({ filteredHashtag, selectedDateRange }) => {
  const [feedPosts, setFeedPosts] = useState([])
  const [loading, setLoading] = useState(true)

  const params = {
    feed: true,
    hashtag: filteredHashtag,
    start_date: selectedDateRange[0]
      ? selectedDateRange[0].toISOString()
      : new Date('1990-01-01').toISOString(),
    end_date: selectedDateRange[0]
      ? selectedDateRange[0].toISOString()
      : new Date('2200-01-01').toISOString(),
  }

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
  }, [filteredHashtag, selectedDateRange])

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
    </CRow>
  )
}

Feed.propTypes = {
  filteredHashtag: PropTypes.string,
  selectedDateRange: PropTypes.array,
}

export default Feed
