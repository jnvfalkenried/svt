import React, { useEffect, useState } from 'react'
import {
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CRow,
  CWidgetStatsF,
  CButton,
  CButtonGroup,
} from '@coreui/react'
import { CChartLine, CChartBar } from '@coreui/react-chartjs'
import CIcon from '@coreui/icons-react'
import { cilCloudDownload, cilUser, cilVideo, cilTag, cilSearch } from '@coreui/icons'
import { getStyle } from '@coreui/utils'

const FetchedData = () => {
  const [stats, setStats] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)
  const [timeRange, setTimeRange] = useState('Month')

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch('http://localhost:80/stats')
        if (!response.ok) {
          throw new Error('Failed to fetch stats')
        }
        const data = await response.json()
        setStats(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
  }, [])

  if (loading) {
    return (
      <CCard>
        <CCardBody>Loading statistics...</CCardBody>
      </CCard>
    )
  }

  if (error) {
    return (
      <CCard className="mb-4">
        <CCardBody className="text-danger">
          <h4>Error</h4>
          <p>{error}</p>
        </CCardBody>
      </CCard>
    )
  }

  const generateLastMonths = (n) => {
    const months = []
    const currentDate = new Date()

    for (let i = n - 1; i >= 0; i--) {
      const date = new Date(currentDate)
      date.setMonth(date.getMonth() - i)
      months.push(date.toLocaleDateString('en-US', { year: 'numeric', month: 'short' }))
    }
    return months
  }

  const generateTrendingData = (numPoints, minValue, maxValue) => {
    const data = []
    let currentValue = minValue

    for (let i = 0; i < numPoints; i++) {
      const increase = (maxValue - minValue) * (0.05 + Math.random() * 0.1)
      currentValue = Math.min(maxValue, currentValue + increase)
      const noise = currentValue * (Math.random() * 0.1 - 0.05)
      data.push(Math.round(currentValue + noise))
    }
    return data
  }

  const timeRangeData = {
    Day: {
      labels: Array.from({ length: 24 }, (_, i) => `${i}:00`),
      postsData: generateTrendingData(24, 50, 200),
      authorsData: generateTrendingData(24, 20, 80),
    },
    Month: {
      labels: generateLastMonths(12),
      postsData: generateTrendingData(12, 1000, 5000),
      authorsData: generateTrendingData(12, 500, 2000),
    },
    Year: {
      labels: Array.from({ length: 5 }, (_, i) => `${2020 + i}`),
      postsData: generateTrendingData(5, 10000, 50000),
      authorsData: generateTrendingData(5, 5000, 20000),
    },
  }

  const lineChartData = {
    labels: timeRangeData[timeRange].labels,
    datasets: [
      {
        label: 'New Posts',
        backgroundColor: `rgba(${getStyle('--cui-info-rgb')}, .1)`,
        borderColor: getStyle('--cui-info'),
        pointHoverBackgroundColor: getStyle('--cui-info'),
        borderWidth: 2,
        data: timeRangeData[timeRange].postsData,
        fill: true,
      },
      {
        label: 'New Authors',
        backgroundColor: `rgba(${getStyle('--cui-success-rgb')}, .1)`,
        borderColor: getStyle('--cui-success'),
        pointHoverBackgroundColor: getStyle('--cui-success'),
        borderWidth: 2,
        data: timeRangeData[timeRange].authorsData,
        fill: true,
      },
    ],
  }

  const metrics = [
    { title: 'Authors', value: stats?.author_count || 0, color: 'info', icon: cilUser },
    { title: 'Posts', value: stats?.post_count || 0, color: 'primary', icon: cilVideo },
    { title: 'Challenges', value: stats?.challenge_count || 0, color: 'warning', icon: cilTag },
    {
      title: 'Active Hashtags',
      value: stats?.active_hashtags_count || 0,
      color: 'danger',
      icon: cilSearch,
    },
  ]

  return (
    <CRow>
      <CCol xs={12}>
        <CRow>
          {metrics.map((metric, index) => (
            <CCol key={index}>
              <CWidgetStatsF
                className="mb-3"
                color={metric.color || 'primary'}
                icon={<CIcon icon={metric.icon} height={24} />}
                title={metric.title}
                value={loading ? 'Loading...' : error ? error : metric.value.toLocaleString()}
              />
            </CCol>
          ))}
        </CRow>

        <CCard className="mb-4">
          <CCardBody>
            <CRow>
              <CCol sm={5}>
                <h4 id="traffic" className="card-title mb-0">
                  Platform Growth
                </h4>
                <div className="small text-body-secondary">
                  {timeRange === 'Day'
                    ? 'Last 24 Hours'
                    : timeRange === 'Month'
                      ? 'Last 12 Months'
                      : 'Last 5 Years'}
                </div>
              </CCol>
              <CCol sm={7} className="d-none d-md-block">
                <CButton color="primary" className="float-end">
                  <CIcon icon={cilCloudDownload} />
                </CButton>
                <CButtonGroup className="float-end me-3">
                  {['Day', 'Month', 'Year'].map((value) => (
                    <CButton
                      color="outline-secondary"
                      key={value}
                      className="mx-0"
                      active={value === timeRange}
                      onClick={() => setTimeRange(value)}
                    >
                      {value}
                    </CButton>
                  ))}
                </CButtonGroup>
              </CCol>
            </CRow>
            <CChartLine
              style={{ height: '300px', marginTop: '40px' }}
              data={lineChartData}
              options={{
                maintainAspectRatio: false,
                plugins: {
                  legend: {
                    display: true,
                  },
                  tooltip: {
                    callbacks: {
                      label: (context) => {
                        let label = context.dataset.label || ''
                        if (label) {
                          label += ': '
                        }
                        label += context.parsed.y.toLocaleString()
                        return label
                      },
                    },
                  },
                },
                scales: {
                  x: {
                    grid: {
                      drawOnChartArea: false,
                    },
                    ticks: {
                      maxRotation: 45,
                      minRotation: 45,
                    },
                  },
                  y: {
                    beginAtZero: true,
                    ticks: {
                      maxTicksLimit: 5,
                      callback: (value) => value.toLocaleString(),
                    },
                  },
                },
                elements: {
                  line: {
                    tension: 0.4,
                  },
                  point: {
                    radius: 2,
                    hitRadius: 10,
                    hoverRadius: 4,
                  },
                },
              }}
            />
          </CCardBody>
        </CCard>

        <CCard className="mb-4">
          <CCardHeader>Content Distribution</CCardHeader>
          <CCardBody>
            <CChartBar
              data={{
                labels: ['Authors', 'Posts', 'Challenges'],
                datasets: [
                  {
                    label: 'Total Count',
                    backgroundColor: [
                      getStyle('--cui-info'),
                      getStyle('--cui-primary'),
                      getStyle('--cui-warning'),
                    ],
                    data: [stats?.author_count, stats?.post_count, stats?.challenge_count],
                  },
                ],
              }}
              options={{
                plugins: {
                  legend: {
                    display: false,
                  },
                },
                scales: {
                  y: {
                    beginAtZero: true,
                  },
                },
              }}
            />
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  )
}

export default FetchedData
