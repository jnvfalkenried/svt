import React from 'react'
import PropTypes from 'prop-types'
import {
  CCard,
  CCardBody,
  CCardHeader,
  CRow,
  CCol,
  CListGroup,
  CListGroupItem,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilBook, cilShieldAlt, cilClock, cilGroup, cibGithub, cibLinkedin } from '@coreui/icons'

// Developer Profile Component
const DeveloperProfile = ({ name, role, github, linkedin, avatar }) => (
  <div className="text-center mb-3">
    <h5 className="mb-1">{name}</h5>
    <p className="text-muted mb-2">{role}</p>
    <div className="d-flex justify-content-center gap-3">
      {github && (
        <a href={github} target="_blank" rel="noopener noreferrer" className="text-dark">
          <CIcon icon={cibGithub} style={{ fontSize: '24px' }} />
        </a>
      )}
      {linkedin && (
        <a href={linkedin} target="_blank" rel="noopener noreferrer" className="text-primary">
          <CIcon icon={cibLinkedin} style={{ fontSize: '24px' }} />
        </a>
      )}
    </div>
  </div>
)

DeveloperProfile.propTypes = {
  name: PropTypes.string.isRequired,
  role: PropTypes.string.isRequired,
  github: PropTypes.string,
  linkedin: PropTypes.string,
  avatar: PropTypes.string.isRequired,
}

const About = () => {
  const developers = [
    {
      name: 'Anand',
      role: 'Data Scientist',
      github: 'https://github.com/janedoe',
      linkedin: 'https://linkedin.com/in/janedoe',
    },
    {
      name: 'Elise Hammarström',
      role: 'Data Scientist',
      github: 'https://github.com/johnsmith',
      linkedin: 'https://linkedin.com/in/johnsmith',
    },
    {
      name: 'Just',
      role: 'Data Scientist',
      github: 'https://github.com/janedoe',
      linkedin: 'https://linkedin.com/in/janedoe',
    },
    {
      name: 'Rustam',
      role: 'Data Scientist',
      github: 'https://github.com/janedoe',
      linkedin: 'https://linkedin.com/in/janedoe',
    },
  ]

  return (
    <CRow className="justify-content-center">
      <CCol md={8}>
        {/* Main Application Info Card */}
        <CCard className="mb-4">
          <CCardHeader>
            <h4 className="m-0">
              <CIcon icon={cilBook} className="me-2" />
              About Hashtag Monitoring Application
            </h4>
          </CCardHeader>
          <CCardBody>
            <p>
              Hashtag Monitoring Application is a comprehensive social media analytics tool designed
              to track and analyze hashtag performance across various platforms
            </p>
            <h5 className="mt-3">Key Features</h5>
            <CListGroup>
              <CListGroupItem>Real-time hashtag tracking</CListGroupItem>
              <CListGroupItem>Comprehensive social media analytics</CListGroupItem>
              <CListGroupItem>Customizable reporting and insights</CListGroupItem>
            </CListGroup>
          </CCardBody>
        </CCard>

        {/* Data Refresh Card */}
        <CCard className="mb-4">
          <CCardHeader>
            <h4 className="m-0">
              <CIcon icon={cilClock} className="me-2" />
              Data Refresh and Synchronization
            </h4>
          </CCardHeader>
          <CCardBody>
            <p>
              Our application fetches the most up-to-date hashtag insights at scheduled intervals:
            </p>
            <ul>
              <li>Hourly data refresh for active hashtags</li>
              <li>Daily comprehensive data synchronization</li>
              <li>Real-time tracking for high-priority tags</li>
            </ul>
          </CCardBody>
        </CCard>

          {/* Project Links Card */}
          <CCard className="mb-4">
          <CCardHeader>
            <h4 className="m-0">Project Links</h4>
          </CCardHeader>
          <CCardBody>
            <h5>Version</h5>
            <p>Hashtag Monitoring Application v1.0.0</p>

            <h5 className="mt-3 mb-2">Resources</h5>
            <div className="d-flex gap-3">
              <a
                href="https://github.com/yourorganization/hashtag-monitoring-app"
                target="_blank"
                rel="noopener noreferrer"
                className="text-decoration-none"
              >
                <CIcon icon={cibGithub} className="me-1" /> GitHub Repository
              </a>
              <a href="/docs" className="text-decoration-none">
                <CIcon icon={cilBook} className="me-1" /> Documentation
              </a>
            </div>
          </CCardBody>
        </CCard>

        {/* Developers Card */}
        <CCard className="mb-4">
          <CCardHeader>
            <h4 className="m-0">
              <CIcon icon={cilGroup} className="me-2" />
              Our Team
            </h4>
          </CCardHeader>
          <CCardBody>
            <CRow>
              {developers.map((dev, index) => (
                <CCol key={index} md={6}>
                  <DeveloperProfile {...dev} />
                </CCol>
              ))}
            </CRow>
          </CCardBody>
        </CCard>

        {/* Licensing Card */}
        <CCard>
          <CCardHeader>
            <h4 className="m-0">
              <CIcon icon={cilShieldAlt} className="me-2" />
              Licensing
            </h4>
          </CCardHeader>
          <CCardBody>
            <p>
              You are free to use, modify, and distribute the software, subject to the terms
              specified in the LICENSE file in our GitHub repository
            </p>
            <a
              href="https://github.com/yourorganization/hashtag-monitoring-app/blob/main/LICENSE"
              target="_blank"
              rel="noopener noreferrer"
            >
              View Full License
            </a>
          </CCardBody>
        </CCard>
      </CCol>
    </CRow>
  )
}

export default About
