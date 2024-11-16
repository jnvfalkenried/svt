import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  CButton,
  CCard,
  CCardBody,
  CCol,
  CContainer,
  CForm,
  CFormInput,
  CInputGroup,
  CInputGroupText,
  CRow,
  CFormCheck,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilLockLocked, cilUser, cilGroup } from '@coreui/icons'

import AuthService from '../../../services/AuthService'

const Register = () => {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [repeatPassword, setRepeatPassword] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [roles, setRoles] = useState([])
  const navigate = useNavigate()

  const validateFields = () => {
    console.log(roles)
    if (!username || !email || !password || !repeatPassword || roles.length === 0) {
      setError('All fields are required')
      return false
    } else {
      setError('')
      return true
    }
  }

  const validatePassword = () => {
    if (password !== repeatPassword) {
      setError('Passwords do not match')
      return false
    } else {
      setError('')
      return true
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()

    // Validate fields
    if (!validateFields()) {
      return
    }

    // Validate password
    if (!validatePassword()) {
      return
    }

    AuthService.register(username, email, password, JSON.stringify(roles))
      .then((response) => {
        setSuccess('Account created successfully. Please login.')

        // Redirect to login page after 2 seconds
        setTimeout(() => {
          navigate('/login')
        }, 2000)
      })
      .catch((error) => {
        if (error.response) {
          console.log('Error in response', error.response)
          setError('An error occurred. Please try again.')
        } else if (error.request) {
          console.log('Error in request', error.request)
          setError('Network error. Please try again.')
        } else {
          console.log('Error in else', error.message)
          setError('An error occurred. Please try again.')
        }
      })
  }

  const handleRoleChange = (role) => {
    setRoles(
      (prevRoles) =>
        prevRoles.includes(role)
          ? prevRoles.filter((r) => r !== role) // Remove role
          : [...prevRoles, role], // Add role
    )
  }

  return (
    <div className="bg-body-tertiary min-vh-100 d-flex flex-row align-items-center">
      <CContainer>
        <CRow className="justify-content-center">
          <CCol md={9} lg={7} xl={6}>
            <CCard className="mx-4">
              <CCardBody className="p-4">
                <CForm onSubmit={handleSubmit}>
                  <h1>Register</h1>
                  <p className="text-body-secondary">Create your account</p>
                  <CInputGroup className="mb-3">
                    <CInputGroupText>
                      <CIcon icon={cilUser} />
                    </CInputGroupText>
                    <CFormInput
                      placeholder="Username"
                      autoComplete="username"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                    />
                  </CInputGroup>
                  <CInputGroup className="mb-3">
                    <CInputGroupText>@</CInputGroupText>
                    <CFormInput
                      placeholder="Email"
                      autoComplete="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                    />
                  </CInputGroup>

                  <CInputGroup className="mb-3">
                    <CInputGroupText>
                      <CIcon icon={cilLockLocked} />
                    </CInputGroupText>
                    <CFormInput
                      type="password"
                      placeholder="Password"
                      autoComplete="new-password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                    />
                  </CInputGroup>
                  <CInputGroup className="mb-4">
                    <CInputGroupText>
                      <CIcon icon={cilLockLocked} />
                    </CInputGroupText>
                    <CFormInput
                      type="password"
                      placeholder="Repeat password"
                      autoComplete="new-password"
                      value={repeatPassword}
                      onChange={(e) => setRepeatPassword(e.target.value)}
                    />
                  </CInputGroup>
                  <CInputGroup className="mb-3">
                    <CInputGroupText>
                      <CIcon icon={cilGroup} />
                    </CInputGroupText>
                    <CCol className="d-flex justify-content-center align-items-center">
                      <CFormCheck
                        inline
                        type="checkbox"
                        id="admin"
                        label="Admin"
                        checked={roles.includes('admin')}
                        onChange={() => handleRoleChange('admin')}
                      />
                      <CFormCheck
                        inline
                        id="user"
                        label="User"
                        checked={roles.includes('user')}
                        onChange={() => handleRoleChange('user')}
                      />
                      <CFormCheck
                        inline
                        type="checkbox"
                        id="dev"
                        label="Dev"
                        checked={roles.includes('dev')}
                        onChange={() => handleRoleChange('dev')}
                      />
                    </CCol>
                  </CInputGroup>
                  {error && (
                    <div className="text-danger mb-3" style={{ textAlign: 'center' }}>
                      {error}
                    </div>
                  )}
                  {success && (
                    <div className="text-success mb-3" style={{ textAlign: 'center' }}>
                      {success}
                    </div>
                  )}
                  <div className="d-grid">
                    <CButton color="success" type="submit">
                      Create Account
                    </CButton>
                  </div>
                </CForm>
              </CCardBody>
            </CCard>
          </CCol>
        </CRow>
      </CContainer>
    </div>
  )
}

export default Register
