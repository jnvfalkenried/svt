import React, { useState } from 'react'
import {
  CRow,
  CCol,
  CFormSelect,
  CNav,
  CNavItem,
  CNavLink,
  CTabContent,
  CTabPane,
  CCard,
  CCardBody,
  CCardHeader,
} from '@coreui/react'
import { CChartBar} from '@coreui/react-chartjs'

// Sample data
const sampleDailyData = {
  '2024-11-15': {
    frequentPosts: [
      { title: 'Funny Video 1', appearances: 20 },
      { title: 'Dance Challenge 2', appearances: 18 },
      { title: 'Cooking Tip 3', appearances: 12 },
    ],
    frequentAuthors: [
      { name: '@funny_creator', appearances: 15 },
      { name: '@dancer_123', appearances: 12 },
      { name: '@chef_4', appearances: 10 },
    ],
    mostViewedPosts: [
      { title: 'Dance Challenge 2', views: 15000 },
      { title: 'Funny Video 1', views: 13000 },
      { title: 'Cooking Tip 3', views: 8000 },
    ],
    mostViewedAuthors: [
      { name: '@dancer_123', views: 50000 },
      { name: '@funny_creator', views: 40000 },
      { name: '@chef_4', views: 25000 },
    ],
  },
  '2024-11-16': {
    frequentPosts: [
      { title: 'Video Clip 4', appearances: 25 },
      { title: 'Challenge 5', appearances: 20 },
      { title: 'Life Hack 6', appearances: 15 },
    ],
    frequentAuthors: [
      { name: '@creator_4', appearances: 18 },
      { name: '@dancer_5', appearances: 15 },
      { name: '@hacker_6', appearances: 12 },
    ],
    mostViewedPosts: [
      { title: 'Challenge 5', views: 20000 },
      { title: 'Video Clip 4', views: 18000 },
      { title: 'Life Hack 6', views: 14000 },
    ],
    mostViewedAuthors: [
      { name: '@dancer_5', views: 55000 },
      { name: '@creator_4', views: 45000 },
      { name: '@hacker_6', views: 30000 },
    ],
  },
}

const sampleWeeklyData = {
  Week1: {
    frequentPosts: [
      { title: 'Compilation 1', appearances: 120 },
      { title: 'Compilation 2', appearances: 100 },
      { title: 'Compilation 3', appearances: 90 },
    ],
    frequentAuthors: [
      { name: '@creator1', appearances: 50 },
      { name: '@creator2', appearances: 45 },
      { name: '@creator3', appearances: 40 },
    ],
    mostViewedPosts: [
      { title: 'Compilation 1', views: 150000 },
      { title: 'Compilation 2', views: 130000 },
      { title: 'Compilation 3', views: 90000 },
    ],
    mostViewedAuthors: [
      { name: '@creator1', views: 200000 },
      { name: '@creator2', views: 180000 },
      { name: '@creator3', views: 120000 },
    ],
  },
  Week2: {
    frequentPosts: [
      { title: 'New Compilation 4', appearances: 140 },
      { title: 'New Compilation 5', appearances: 130 },
      { title: 'New Compilation 6', appearances: 110 },
    ],
    frequentAuthors: [
      { name: '@creator4', appearances: 60 },
      { name: '@creator5', appearances: 55 },
      { name: '@creator6', appearances: 50 },
    ],
    mostViewedPosts: [
      { title: 'New Compilation 4', views: 160000 },
      { title: 'New Compilation 5', views: 140000 },
      { title: 'New Compilation 6', views: 100000 },
    ],
    mostViewedAuthors: [
      { name: '@creator4', views: 220000 },
      { name: '@creator5', views: 200000 },
      { name: '@creator6', views: 150000 },
    ],
  },
}

const Reports = () => {
  const [activeTab, setActiveTab] = useState('daily')
  const [selectedDate, setSelectedDate] = useState('2024-11-15')
  const [selectedWeek, setSelectedWeek] = useState('Week1')

  const isDaily = activeTab === 'daily'
  const data = isDaily ? sampleDailyData[selectedDate] : sampleWeeklyData[selectedWeek]

  // Extract data for charts
  const frequentPostLabels = data.frequentPosts.map((post) => post.title)
  const frequentPostValues = data.frequentPosts.map((post) => post.appearances)

  const frequentAuthorLabels = data.frequentAuthors.map((author) => author.name)
  const frequentAuthorValues = data.frequentAuthors.map((author) => author.appearances)

  const mostViewedPostLabels = data.mostViewedPosts.map((post) => post.title)
  const mostViewedPostValues = data.mostViewedPosts.map((post) => post.views)

  const mostViewedAuthorLabels = data.mostViewedAuthors.map((author) => author.name)
  const mostViewedAuthorValues = data.mostViewedAuthors.map((author) => author.views)

  return (
    <div>
      <h1 className="mb-4">TikTok Reports</h1>

      {/* Tabs for Daily and Weekly */}
      <CNav variant="tabs" role="tablist" className="mb-4">
        <CNavItem>
          <CNavLink active={activeTab === 'daily'} onClick={() => setActiveTab('daily')}>
            Daily
          </CNavLink>
        </CNavItem>
        <CNavItem>
          <CNavLink active={activeTab === 'weekly'} onClick={() => setActiveTab('weekly')}>
            Weekly
          </CNavLink>
        </CNavItem>
      </CNav>

      {/* Date/Week Selector */}
      <CFormSelect
        className="mb-4"
        value={isDaily ? selectedDate : selectedWeek}
        onChange={(e) =>
          isDaily ? setSelectedDate(e.target.value) : setSelectedWeek(e.target.value)
        }
      >
        {isDaily
          ? Object.keys(sampleDailyData).map((date) => (
              <option key={date} value={date}>
                {date}
              </option>
            ))
          : Object.keys(sampleWeeklyData).map((week) => (
              <option key={week} value={week}>
                {week}
              </option>
            ))}
      </CFormSelect>

      <CTabContent>
        <CTabPane visible={activeTab === 'daily' || activeTab === 'weekly'}>
          {/* Combined Most Frequent Posts and Authors */}
          <CCard className="mb-4">
            <CCardHeader>Most Frequent in Feed</CCardHeader>
            <CCardBody>
              <CRow>
                {/* Most Frequent Posts */}
                <CCol md={6}>
                  <h5>Posts</h5>
                  <CChartBar
                    data={{
                      labels: frequentPostLabels,
                      datasets: [
                        {
                          label: 'Appearances',
                          backgroundColor: '#007bff',
                          data: frequentPostValues,
                        },
                      ],
                    }}
                  />
                </CCol>
                {/* Most Frequent Authors */}
                <CCol md={6}>
                  <h5>Authors</h5>
                  <CChartBar
                    data={{
                      labels: frequentAuthorLabels,
                      datasets: [
                        {
                          label: 'Appearances',
                          backgroundColor: '#28a745',
                          data: frequentAuthorValues,
                        },
                      ],
                    }}
                  />
                </CCol>
              </CRow>
            </CCardBody>
          </CCard>

          {/* Combined Most Viewed Posts and Authors */}
          <CCard className="mb-4">
            <CCardHeader>Most Viewed</CCardHeader>
            <CCardBody>
              <CRow>
                {/* Most Viewed Posts */}
                <CCol md={6}>
                  <h5>Posts</h5>
                  <CChartBar
                    data={{
                      labels: mostViewedPostLabels,
                      datasets: [
                        {
                          label: 'Views',
                          borderColor: '#007bff',
                          backgroundColor: '#007bff',
                          data: mostViewedPostValues,
                        },
                      ],
                    }}
                  />
                </CCol>

                {/* Most Viewed Authors */}
                <CCol md={6}>
                  <h5>Authors</h5>
                  <CChartBar
                    data={{
                      labels: mostViewedAuthorLabels,
                      datasets: [
                        {
                          label: 'Views',
                          borderColor: '#28a745',
                          backgroundColor: '#28a745',
                          data: mostViewedAuthorValues,
                        },
                      ],
                    }}
                  />
                </CCol>
              </CRow>
            </CCardBody>
          </CCard>
        </CTabPane>
      </CTabContent>
    </div>
  )
}

export default Reports
