import React, { useEffect, useState } from 'react'
import { CCard, CCardBody, CCol, CRow, CWidgetStatsF, CButton, CButtonGroup } from '@coreui/react'
import { CChartLine, CChartBar } from '@coreui/react-chartjs'
import CIcon from '@coreui/icons-react'
import { cilUser, cilVideo, cilTag, cilSearch } from '@coreui/icons'
import { getStyle } from '@coreui/utils'
import ApiService from '../../services/ApiService'

const FetchedData = () => {
  const [stats, setStats] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)
  const [timeRange, setTimeRange] = useState('Day')
  const [platformGrowth, setPlatformGrowth] = useState(null)

  useEffect(() => {
    ApiService.getStats().then(
      (response) => {
        setStats(response.data)
        setLoading(false)
      },
      (error) => {
        setError('Failed to fetch statistics')
        console.error(error)
        setLoading(false)
      },
    )
  }, [])

  useEffect(() => {
    ApiService.getPlatformGrowth({ interval: timeRange })
      .then((response) => {
        setPlatformGrowth(response.data)
      })
      .catch((error) => {
        setError('Failed to fetch platform growth data')
        console.error(error)
      })
  }, [timeRange])

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

  const unionLabels = platformGrowth
    ? [
        ...new Set([
          ...platformGrowth.author_growth.map((data) => data.interval),
          ...platformGrowth.post_growth.map((data) => data.interval),
          ...platformGrowth.challenge_growth.map((data) => data.interval),
        ]),
      ]
    : []

  const getGrowthDataForLabel = (growthData, label) => {
    const dataPoint = growthData.find((data) => data.interval === label)
    return dataPoint ? dataPoint.count : 0
  }

  const lineChartData = {
    labels: unionLabels,
    datasets: [
      {
        label: 'New Posts',
        backgroundColor: `rgba(${getStyle('--cui-info-rgb')}, .3)`,
        borderColor: getStyle('--cui-info'),
        pointHoverBackgroundColor: getStyle('--cui-info'),
        borderWidth: 2,
        data: unionLabels.map((label) => getGrowthDataForLabel(platformGrowth.post_growth, label)),
        fill: true,
      },
      {
        label: 'New Authors',
        backgroundColor: `rgba(${getStyle('--cui-success-rgb')}, .3)`,
        borderColor: getStyle('--cui-success'),
        pointHoverBackgroundColor: getStyle('--cui-success'),
        borderWidth: 2,
        data: unionLabels.map((label) =>
          getGrowthDataForLabel(platformGrowth.author_growth, label),
        ),
        fill: true,
      },
      {
        label: 'New Hashtags',
        backgroundColor: `rgba(${getStyle('--cui-warning-rgb')}, .3)`,
        borderColor: getStyle('--cui-warning'),
        pointHoverBackgroundColor: getStyle('--cui-warning'),
        borderWidth: 2,
        data: unionLabels.map((label) =>
          getGrowthDataForLabel(platformGrowth.challenge_growth, label),
        ),
        fill: true,
      },
    ],
  }

  const lineChartOptions = {
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
      },
    },
    scales: {
      x: {
        grid: {
          drawOnChartArea: false,
        },
      },
      y: {
        beginAtZero: true,
        ticks: {
          maxTicksLimit: 5,
        },
      },
    },
    elements: {
      line: {
        tension: 0.4,
      },
      point: {
        radius: 0,
        hitRadius: 10,
        hoverRadius: 4,
      },
    },
  }

  const aggregateData = (data, category) => {
    return data.reduce((total, item) => total + (item[category] || 0), 0)
  }

  const totalAuthors = platformGrowth ? aggregateData(platformGrowth.author_growth, 'count') : 0
  const totalPosts = platformGrowth ? aggregateData(platformGrowth.post_growth, 'count') : 0
  const totalChallenges = platformGrowth
    ? aggregateData(platformGrowth.challenge_growth, 'count')
    : 0

  const barChartData = {
    labels: ['Authors', 'Posts', 'Challenges'],
    datasets: [
      {
        label: 'Total Count',
        backgroundColor: [
          getStyle('--cui-info'),
          getStyle('--cui-primary'),
          getStyle('--cui-warning'),
        ],
        data: [totalAuthors, totalPosts, totalChallenges],
      },
    ],
  }

  const barChartOptions = {
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
  }

  const metrics = [
    {
      color: 'primary',
      icon: cilUser,
      title: 'Authors',
      value: stats?.author_count || 0,
    },
    {
      color: 'info',
      icon: cilVideo,
      title: 'Posts',
      value: stats?.post_count || 0,
    },
    {
      color: 'success',
      icon: cilSearch,
      title: 'Collected Hashtags',
      value: stats?.challenge_count || 0,
    },
    {
      color: 'warning',
      icon: cilTag,
      title: 'Active Hashtags',
      value: stats?.active_hashtags_count || 0,
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
                <h4 id="platform-growth" className="card-title mb-0">
                  Platform Growth
                </h4>
              </CCol>
              <CCol sm={7} className="d-none d-md-block">
                <CButtonGroup className="float-end me-3">
                  {['Day', 'Week', 'Month', 'Year'].map((value) => (
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
              options={lineChartOptions}
            />
          </CCardBody>
        </CCard>

        <CCard className="mb-4">
          <CCardBody>
            <CRow>
              <CCol sm={5}>
                <h4 id="platform-growth" className="card-title mb-4">
                  Content Distribution
                </h4>
              </CCol>
            </CRow>
            <CChartBar data={barChartData} options={barChartOptions} />
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  )
}

export default FetchedData
