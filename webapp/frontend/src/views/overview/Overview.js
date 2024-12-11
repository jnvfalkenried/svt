import React from 'react'
import { useEffect, useState } from 'react'

import { CWidgetStatsF, CCol, CRow, CCardBody, CCard } from '@coreui/react'

import CIcon from '@coreui/icons-react'

import { cilUser, cilVideo, cilSearch, cilTag } from '@coreui/icons'

import MainChart from './MainChart'

import ApiService from '../../services/ApiService'

const Overview = () => {
  const [stats, setStats] = useState({
    author_count: 0,
    post_count: 0,
    challenge_count: 0,
    active_hashtags_count: 0,
  })
  const [authors, setAuthors] = useState([])
  const [loadingStats, setLoadingStats] = useState(true)
  const [errorStats, setErrorStats] = useState(null)
  const [loadingAuthors, setLoadingAuthors] = useState(true)
  const [errorAuthors, setErrorAuthors] = useState(null)

  useEffect(() => {
    // Call the FastAPI stats endpoint
    fetch('/api/stats')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch stats')
        }
        return response.json()
      })
      .then((data) => {
        setStats(data)
        setLoadingStats(false)
      })
      .catch((error) => {
        setErrorStats(error.message)
        setLoadingStats(false)
      })
  }, [stats, loadingStats, errorStats])

  useEffect(() => {
    ApiService.top_authors()
      .then((response) => {
        setAuthors(response.data)
        setLoadingAuthors(false)
      })
      .catch((error) => {
        setErrorAuthors(error.message)
        setLoadingAuthors(false)
      })
  }, [authors, loadingAuthors, errorAuthors])

  return (
    <>
      <CRow>
        <CCol>
          <CWidgetStatsF
            className="mb-3"
            color="primary"
            icon={<CIcon icon={cilUser} height={24} />}
            title="Authors"
            value={loadingStats ? 'Loading...' : errorStats ? errorStats : stats.author_count}
          />
        </CCol>
        <CCol>
          <CWidgetStatsF
            className="mb-3"
            color="primary"
            icon={<CIcon icon={cilVideo} height={24} />}
            title="TikTok Posts"
            value={loadingStats ? 'Loading...' : errorStats ? errorStats : stats.post_count}
          />
        </CCol>
        <CCol>
          <CWidgetStatsF
            className="mb-3"
            color="primary"
            icon={<CIcon icon={cilTag} height={24} />}
            title="Challenges"
            value={loadingStats ? 'Loading...' : errorStats ? errorStats : stats.challenge_count}
          />
        </CCol>
        <CCol>
          <CWidgetStatsF
            className="mb-3"
            color="primary"
            icon={<CIcon icon={cilSearch} height={24} />}
            title="Actvie Hashtags"
            value={
              loadingStats ? 'Loading...' : errorStats ? errorStats : stats.active_hashtags_count
            }
          />
        </CCol>
      </CRow>
      <CCard className="mb-4">
        <CCardBody>
          <CRow>
            <CCol>
              <h4>Top Authors</h4>
              <div className="small text-body-secondary">
                Most successful TikTok authors in DB in regards to follower count
              </div>
            </CCol>
          </CRow>
          {loadingAuthors ? (
            'Loading...'
          ) : errorAuthors ? (
            errorAuthors
          ) : (
            <MainChart data={authors} />
          )}
        </CCardBody>
      </CCard>
    </>
  )
}

export default Overview
