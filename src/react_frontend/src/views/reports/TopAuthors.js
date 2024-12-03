import React, { useState, useEffect, useRef, useMemo } from 'react'
import { getStyle } from '@coreui/utils'
import PropTypes from 'prop-types'
import ApiService from '../../services/ApiService'
import { CRow, CCol, CCard, CCardBody, CButton, CButtonGroup } from '@coreui/react'
import { CChartBar } from '@coreui/react-chartjs'
import AuthorDetailsOffcanvas from './AuthorDetailsOffcanvas'
import { cilVideo } from '@coreui/icons'
import CIcon from '@coreui/icons-react'

const TopAuthors = ({ params }) => {
  const categories = ['Likes Collected', 'Likes Given', 'Followers', 'Videos']
  const [topAuthors, setTopAuthors] = useState({})
  const [loading, setLoading] = useState(true)
  const [offcanvasVisible, setOffcanvasVisible] = useState(false)
  const [selectedAuthor, setSelectedAuthor] = useState(null)
  const [activeCategory, setActiveCategory] = useState('Likes Collected')
  const activeAuthors = topAuthors[activeCategory] || []

  const topAuthorsRef = useRef({})

  useEffect(() => {
    const fetchTopAuthors = async () => {
      try {
        const newTopAuthors = {}
        for (const el of categories) {
          const response = await ApiService.getTopAuthors({ ...params, category: el })
          newTopAuthors[el] = response.data
        }
        setTopAuthors(newTopAuthors)
      } catch (error) {
        console.error(error)
      } finally {
        setLoading(false)
      }
    }

    fetchTopAuthors()
  }, [params])

  useEffect(() => {
    topAuthorsRef.current = topAuthors
  }, [topAuthors])

  const handleBarClick = (event) => {
    const activePoints = event.chart.getElementsAtEventForMode(
      event.native,
      'nearest',
      { intersect: true },
      true,
    )
    if (activePoints.length > 0) {
      const dataIndex = activePoints[0].index
      const post = topAuthorsRef.current[activeCategory][dataIndex]

      if (post) {
        setSelectedAuthor(post)
        setOffcanvasVisible(true)
      }
    }
  }

  // Prepare chart data based on the active category
  const chartData = useMemo(
    () => ({
      labels: activeAuthors.map((author) => author.nickname),
      datasets: [
        {
          label: activeCategory,
          backgroundColor: `rgba(${getStyle('--cui-info-rgb')}, .7)`,
          borderColor: getStyle('--cui-info'),
          data: activeAuthors.map((author) => {
            switch (activeCategory) {
              case 'Likes Collected':
                return author.max_heart_count
              case 'Likes Given':
                return author.max_digg_count
              case 'Followers':
                return author.max_follower_count
              case 'Videos':
                return author.max_video_count
              default:
                return author.max_heart_count
            }
          }),
          hoverBackgroundColor: getStyle('--cui-info'),
          hoverBorderColor: getStyle('--cui-info'),
        },
      ],
    }),
    [activeAuthors, activeCategory],
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
            const post = activeAuthors[tooltipItem.dataIndex]
            return [
              //`Description: ${post.description}`,
              //` Plays: ${post.max_play_count}`,
              ` Likes: ${post.max_heart_count}`,
              //` Likes Give: ${post.max_comment_count}`,
              ` Follower: ${post.max_follower_count}`,
              ` Videos: ${post.max_video_count}`,
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
      <AuthorDetailsOffcanvas
        visible={offcanvasVisible}
        onClose={() => setOffcanvasVisible(false)}
        author={selectedAuthor}
      />
    </CRow>
  )
}

TopAuthors.propTypes = {
  params: PropTypes.object.isRequired,
}

export default TopAuthors
