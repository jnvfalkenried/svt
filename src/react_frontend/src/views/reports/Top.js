import React, { useState, useEffect } from 'react'
import PropTypes from 'prop-types'
import ApiService from '../../services/ApiService'
import { getStyle } from '@coreui/utils'
import { CRow, CCol, CCard, CCardBody, CCardHeader } from '@coreui/react'
import { CChartBar } from '@coreui/react-chartjs'
import { CIcon } from '@coreui/icons-react'
import { cilVideo } from '@coreui/icons'

const Top = ({ filteredHashtag, selectedDateRange }) => {
  const [topPosts, setTopPosts] = useState([])
  const [loading, setLoading] = useState(true)

  const params = {
    feed: false,
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
        setTopPosts(response.data)
        setLoading(false)
        console.log(response.data)
      })
      .catch((error) => {
        console.log(error)
        setLoading(false)
      })
  }, [filteredHashtag, selectedDateRange])

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
    </CRow>
  )
}

Top.propTypes = {
  filteredHashtag: PropTypes.string,
  selectedDateRange: PropTypes.array,
}

export default Top
