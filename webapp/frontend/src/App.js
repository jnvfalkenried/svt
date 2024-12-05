import React, { Suspense, useEffect } from 'react'
import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom'
import { useSelector, useDispatch } from 'react-redux'
import { jwtDecode } from 'jwt-decode'

import { CSpinner, useColorModes } from '@coreui/react'
import './scss/style.scss'

// Containers
const DefaultLayout = React.lazy(() => import('./layout/DefaultLayout'))

// Pages
const Login = React.lazy(() => import('./views/pages/login/Login'))
const Register = React.lazy(() => import('./views/pages/register/Register'))
const Page404 = React.lazy(() => import('./views/pages/page404/Page404'))
const Page500 = React.lazy(() => import('./views/pages/page500/Page500'))
const ForgotPassword = React.lazy(() => import('./views/pages/forgot_password/ForgotPassword'))

const App = () => {
  const { isColorModeSet, setColorMode } = useColorModes('coreui-free-react-admin-template-theme')
  const storedTheme = useSelector((state) => state.theme)
  const token = useSelector((state) => state.access_token)
  const dispatch = useDispatch()

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.href.split('?')[1])
    const theme = urlParams.get('theme') && urlParams.get('theme').match(/^[A-Za-z0-9\s]+/)[0]
    if (theme) {
      setColorMode(theme)
    }

    if (isColorModeSet()) {
      return
    }

    setColorMode(storedTheme)
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    const isLoggedIn = localStorage.getItem('access_token')
    if (!isLoggedIn) return
    const tokenCheckInterval = setInterval(() => {
      const token = localStorage.getItem('access_token') // Ensure you get the latest token
      if (token) {
        const decoded = jwtDecode(token)
        const currentTime = Date.now() / 1000
        if (decoded.exp < currentTime) {
          console.log('Token expired. Logging out...')
          dispatch({ type: 'set', access_token: null })
          localStorage.removeItem('access_token')
          window.location.href = '/login' // Redirect user to login
        }
      } else {
        console.log('No token found. Logging out...')
        dispatch({ type: 'set', access_token: null })
        window.location.href = '/login'
      }
    }, 10000) // Check every 10 seconds

    return () => clearInterval(tokenCheckInterval) // Clear the interval on unmount
  }, [dispatch])

  const isAuthenticated = () => {
    if (token) {
      const decoded = jwtDecode(token)
      const currentTime = Date.now() / 1000
      if (decoded.exp < currentTime) {
        dispatch({ type: 'set', access_token: null })
        localStorage.removeItem('access_token')
        return false
      }
      return true
    }
    dispatch({ type: 'set', access_token: null })
    localStorage.removeItem('access_token')
    return false
  }

  return (
    <BrowserRouter>
      <Suspense
        fallback={
          <div className="pt-3 text-center">
            <CSpinner color="primary" variant="grow" />
          </div>
        }
      >
        <Routes>
          {/* Authentication Check */}
          {!isAuthenticated() ? (
            <Route exact path="*" element={<Navigate to="/login" replace />} />
          ) : (
            <>
              {/* Authenticated Routes */}
              {/*<Route exact path="/" name="Home" element={<DefaultLayout />} />*/}
              <Route exact path="/404" name="Page 404" element={<Page404 />} />
              <Route exact path="/500" name="Page 500" element={<Page500 />} />
              <Route path="*" name="Home" element={<DefaultLayout />} />
            </>
          )}

          {/* Public Login Route */}
          <Route exact path="/login" name="Login Page" element={<Login />} />
          <Route exact path="/register" name="Register Page" element={<Register />} />
          <Route
            exact
            path="/forgot-password"
            name="Forgot Password Page"
            element={<ForgotPassword />}
          />
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}

export default App
