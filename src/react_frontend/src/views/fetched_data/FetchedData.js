import React, { useEffect, useState } from 'react'
import {
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CRow,
  CProgress,
  CButton,
  CButtonGroup,
} from '@coreui/react'
import { CChartLine, CChartBar } from '@coreui/react-chartjs'
import CIcon from '@coreui/icons-react'
import { cilCloudDownload } from '@coreui/icons'
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

  const metrics = [
    { title: 'Authors', value: stats?.author_count || 0, color: 'info' },
    { title: 'Posts', value: stats?.post_count || 0, color: 'primary' },
    { title: 'Challenges', value: stats?.challenge_count || 0, color: 'warning' },
  ]

  const lineChartData = {
    labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
    datasets: [
      {
        label: 'New Posts',
        backgroundColor: `rgba(${getStyle('--cui-info-rgb')}, .1)`,
        borderColor: getStyle('--cui-info'),
        pointHoverBackgroundColor: getStyle('--cui-info'),
        borderWidth: 2,
        data: [50, 60, 70, 85, 90, 100, 110],
        fill: true,
      },
      {
        label: 'New Authors',
        backgroundColor: 'transparent',
        borderColor: getStyle('--cui-success'),
        pointHoverBackgroundColor: getStyle('--cui-success'),
        borderWidth: 2,
        data: [20, 25, 30, 35, 40, 45, 50],
      },
    ],
  }

  return (
    <CRow>
      <CCol xs={12}>
        <CRow xs={{ cols: 1 }} md={{ cols: 2 }} xl={{ cols: 4 }} className="mb-4">
          {metrics.map((metric, index) => (
            <CCol key={index}>
              <CCard className="mb-4">
                <CCardBody>
                  <div className="fs-4 fw-semibold">{metric.value.toLocaleString()}</div>
                  <div className="text-body-secondary text-truncate">{metric.title}</div>
                  <CProgress thin className="mt-3" color={metric.color} value={100} />
                </CCardBody>
              </CCard>
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
                <div className="small text-body-secondary">January - July 2023</div>
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
