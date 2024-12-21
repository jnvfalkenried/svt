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
      name: 'Anand Mathew M S',
      role: 'Data Scientist',
      github: 'https://github.com/anandmatt',
      linkedin: 'https://www.linkedin.com/in/anand-mathew-m-s-34a135176/',
    },
    {
      name: 'Elise Hammarström',
      role: 'Data Scientist',
      github: 'https://github.com/elisehammarstrom',
      linkedin: 'https://www.linkedin.com/in/elise-hammarstrom/',
    },
    {
      name: 'Just Niklas von Falkenried',
      role: 'Data Scientist',
      github: 'https://github.com/jnvfalkenried',
      linkedin: 'https://www.linkedin.com/in/just-niklas-von-falkenried/',
    },
    {
      name: 'Rustam Ismailov',
      role: 'Data Scientist',
      github: 'https://github.com/Ftalysh',
      linkedin: 'https://www.linkedin.com/in/rustam-ismailov/',
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
          <p className="text-justify">
          Our TikTok Data Monitoring Application provides a streamlined, open-source solution for comprehensive content retrieval and analysis. Designed with both user-friendliness and technical flexibility in mind, the platform offers an intuitive interface and a customizable technical architecture that developers can easily extend and adapt to specific needs.
          </p>
            <h5 className="mt-3">Key Features</h5>
            <CListGroup>
              <CListGroupItem>Comprehensive TikTok Content Retrieval</CListGroupItem>
              <CListGroupItem>Hashtag Tracking</CListGroupItem>
              <CListGroupItem>Advanced Image and Content Search</CListGroupItem>
              <CListGroupItem>Direct Content Linking</CListGroupItem>
              <CListGroupItem>Open-Source and Customizable Architecture</CListGroupItem>
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
          Our application fetches the most up-to-date hashtag insights through a sophisticated scheduling mechanism:
        </p>
        <ul>
          <li>Hashtag monitoring updates every 30 minutes</li>
          <li>Processing retrieved content at 00:01, 08:01, and 16:01</li>
          <li>Post trends view refresh at 01:00, 09:00, and 17:00</li>
          <li>Author trends view refresh at 01:05, 09:05, and 17:05</li>
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
