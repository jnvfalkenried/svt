import React, { useEffect, useState } from 'react'
import { jwtDecode } from 'jwt-decode'
import { useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import {
  CAvatar,
  CBadge,
  CDropdown,
  CDropdownDivider,
  CDropdownHeader,
  CDropdownItem,
  CDropdownMenu,
  CDropdownToggle,
} from '@coreui/react'
import {
  cilBell,
  cilCreditCard,
  cilCommentSquare,
  cilEnvelopeOpen,
  cilFile,
  cilLockLocked,
  cilSettings,
  cilTask,
  cilUser,
  cilAccountLogout,
} from '@coreui/icons'
import CIcon from '@coreui/icons-react'

const AppHeaderDropdown = () => {
  const navigate = useNavigate()
  const handleLogout = () => {
    // Remove the authentication state from localStorage
    localStorage.removeItem('access_token')
    // Redirect to login page
    navigate('/api/login')
  }
  const devMode = useSelector((state) => state.dev)
  const [userInitials, setUserInitials] = useState('')

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (!token) return
    const decoded = jwtDecode(token)
    // Set the user's initials if username is defined and has at least two characters
    if (decoded.username && decoded.username.length >= 2) {
      setUserInitials(`${decoded.username[0].toUpperCase()}${decoded.username[1].toUpperCase()}`)
    } else {
      setUserInitials(decoded.username ? decoded.username[0].toUpperCase() : '')
    }
  }, [])

  return (
    <CDropdown variant="nav-item">
      <CDropdownToggle placement="bottom-end" className="py-0 pe-0" caret={false}>
        <CAvatar size="md" color="secondary" textColor="white">
          {userInitials}
        </CAvatar>
      </CDropdownToggle>
      <CDropdownMenu className="pt-0" placement="bottom-end">
        {devMode && (
          <div>
            <CDropdownHeader className="bg-body-secondary fw-semibold mb-2">
              Account
            </CDropdownHeader>
            <CDropdownItem href="#">
              <CIcon icon={cilBell} className="me-2" />
              Updates
              <CBadge color="info" className="ms-2">
                42
              </CBadge>
            </CDropdownItem>
            <CDropdownItem href="#">
              <CIcon icon={cilEnvelopeOpen} className="me-2" />
              Messages
              <CBadge color="success" className="ms-2">
                42
              </CBadge>
            </CDropdownItem>
            <CDropdownItem href="#">
              <CIcon icon={cilTask} className="me-2" />
              Tasks
              <CBadge color="danger" className="ms-2">
                42
              </CBadge>
            </CDropdownItem>
            <CDropdownItem href="#">
              <CIcon icon={cilCommentSquare} className="me-2" />
              Comments
              <CBadge color="warning" className="ms-2">
                42
              </CBadge>
            </CDropdownItem>
            <CDropdownHeader className="bg-body-secondary fw-semibold my-2">
              Settings
            </CDropdownHeader>
            <CDropdownItem href="#">
              <CIcon icon={cilUser} className="me-2" />
              Profile
            </CDropdownItem>
            <CDropdownItem href="#">
              <CIcon icon={cilSettings} className="me-2" />
              Settings
            </CDropdownItem>
            <CDropdownItem href="#">
              <CIcon icon={cilCreditCard} className="me-2" />
              Payments
              <CBadge color="secondary" className="ms-2">
                42
              </CBadge>
            </CDropdownItem>
            <CDropdownItem href="#">
              <CIcon icon={cilFile} className="me-2" />
              Projects
              <CBadge color="primary" className="ms-2">
                42
              </CBadge>
            </CDropdownItem>
            <CDropdownDivider />
            <CDropdownItem href="#">
              <CIcon icon={cilLockLocked} className="me-2" />
              Lock Account
            </CDropdownItem>
          </div>
        )}
        <CDropdownItem href="#" onClick={handleLogout}>
          <CIcon icon={cilAccountLogout} className="me-2" />
          Logout
        </CDropdownItem>
      </CDropdownMenu>
    </CDropdown>
  )
}

export default AppHeaderDropdown
