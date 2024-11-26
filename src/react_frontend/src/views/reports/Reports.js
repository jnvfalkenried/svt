import React, { useState, useEffect } from 'react'
import {
  CFormSelect,
  CNav,
  CNavItem,
  CNavLink,
  CTabContent,
  CTabPane,
  CCol,
  CRow,
} from '@coreui/react'
import ApiService from '../../services/ApiService'
import Feed from './Feed'
import Top from './Top'
import Filters from './Filters'

const Reports = () => {
  const [activeTab, setActiveTab] = useState('top')
  const [hashtags, setHashtags] = useState([])
  const [selectedHashtag, setSelectedHashtag] = useState('all')
  const [selectedDateRange, setSelectedDateRange] = useState([null, null])

  useEffect(() => {
    ApiService.getActiveHashtags()
      .then((response) => {
        setHashtags(response.data)
      })
      .catch((error) => {
        console.error(error)
      })
  }, [])

  return (
    <div>
      {/* Tabs for Daily and Weekly */}
      <CNav variant="tabs" role="tablist" className="mb-4">
        <CNavItem>
          <CNavLink
            active={activeTab === 'top'}
            onClick={() => setActiveTab('top')}
            style={{ cursor: 'pointer' }}
          >
            Top Posts
          </CNavLink>
        </CNavItem>
        <CNavItem>
          <CNavLink
            active={activeTab === 'feed'}
            onClick={() => setActiveTab('feed')}
            style={{ cursor: 'pointer' }}
          >
            Feed
          </CNavLink>
        </CNavItem>
      </CNav>

      {/* Filters */}
      <Filters
        hashtags={hashtags}
        selectedHashtag={selectedHashtag}
        setSelectedHashtag={setSelectedHashtag}
        onDateRangeChange={setSelectedDateRange}
      />

      <CTabContent>
        {/* Top Posts */}
        <CTabPane visible={activeTab === 'top'}>
          <Top filteredHashtag={selectedHashtag} selectedDateRange={selectedDateRange} />
        </CTabPane>
        {/* Feed */}
        <CTabPane visible={activeTab === 'feed'}>
          <Feed filteredHashtag={selectedHashtag} selectedDateRange={selectedDateRange} />
        </CTabPane>
      </CTabContent>
    </div>
  )
}

export default Reports
