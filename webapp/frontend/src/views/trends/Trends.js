import React, { useState } from 'react'
import {
  CCard,
  CCardHeader,
  CCardBody,
  CNav,
  CNavItem,
  CNavLink,
  CTabContent,
  CTabPane,
} from '@coreui/react'
import PostTrendsTable from './PostTrendsTable'
import AuthorTrendsTable from './AuthorTrendsTable'

const Trends = () => {
  const [activeTab, setActiveTab] = useState(1)

  return (
    <CCard className="mb-4">
      <CCardHeader>
        <CNav variant="tabs">
          <CNavItem>
            <CNavLink
              active={activeTab === 1}
              onClick={() => setActiveTab(1)}
              style={{ cursor: 'pointer' }}
            >
              Post Growth Trends
            </CNavLink>
          </CNavItem>
          <CNavItem>
            <CNavLink
              active={activeTab === 2}
              onClick={() => setActiveTab(2)}
              style={{ cursor: 'pointer' }}
            >
              Author Growth Trends
            </CNavLink>
          </CNavItem>
        </CNav>
      </CCardHeader>
      <CCardBody>
        <CTabContent>
          <CTabPane visible={activeTab === 1}>
            <PostTrendsTable />
          </CTabPane>
          <CTabPane visible={activeTab === 2}>
            <AuthorTrendsTable />
          </CTabPane>
        </CTabContent>
      </CCardBody>
    </CCard>
  )
}

export default Trends
