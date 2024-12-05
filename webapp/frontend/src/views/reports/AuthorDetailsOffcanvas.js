import React from 'react'
import PropTypes from 'prop-types'
import {
  COffcanvas,
  COffcanvasHeader,
  COffcanvasTitle,
  COffcanvasBody,
  CCloseButton,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import {
  cilMediaPlay,
  cilHeart,
  cilUser,
  cilCheckCircle,
  cilBookmark,
  cilLink,
  cilCalendar,
  cilDescription,
  cilGroup,
} from '@coreui/icons'

const AuthorDetailsOffcanvas = ({ visible, onClose, author }) => {
  const authorUniqueId = author?.unique_id || 'unknown-author' // Provide a fallback value
  const tiktokUrl = `https://www.tiktok.com/@${authorUniqueId || 'unknown-id'}`

  const formatNumber = (number) => {
    if (number >= 1_000_000) {
      return `${(number / 1_000_000).toFixed(1)}M`
    } else if (number >= 1_000) {
      return `${(number / 1_000).toFixed(1)}K`
    }
    return number.toString()
  }

  return (
    <COffcanvas placement="end" visible={visible} onHide={onClose} style={{ width: '30%' }}>
      <COffcanvasHeader>
        <COffcanvasTitle>
          <strong>Author Details</strong>
        </COffcanvasTitle>
        <CCloseButton className="text-reset" onClick={onClose} />
      </COffcanvasHeader>
      <COffcanvasBody>
        {author ? (
          <div>
            <p>
              <CIcon icon={cilUser} className="me-2 text-muted" /> <strong>Nickname:</strong>{' '}
              {author.nickname}
            </p>
            <p>
              <CIcon icon={cilDescription} className="me-2 text-muted" />
              <strong>Signature:</strong> {author.signature || 'No signature available'}
            </p>
            <p>
              <CIcon
                icon={cilCheckCircle}
                className={`me-2 ${author.verified ? 'text-success' : 'text-danger'}`}
              />
              <strong>Verified:</strong> {author.verified ? 'Yes' : 'No'}
            </p>
            <p>
              <CIcon icon={cilCalendar} className="me-2 text-muted" />{' '}
              <strong>Last Collected At:</strong> {author.last_collected_at}
            </p>
            <p>
              <CIcon icon={cilMediaPlay} className="me-2" /> <strong>Videos:</strong>{' '}
              {formatNumber(author.max_video_count)}
            </p>
            <p>
              <CIcon icon={cilHeart} className="me-2 text-danger" /> <strong>Hearts:</strong>{' '}
              {formatNumber(author.max_heart_count)}
            </p>
            <p>
              <CIcon icon={cilBookmark} className="me-2 text-warning" /> <strong>Followers:</strong>{' '}
              {formatNumber(author.max_follower_count)}
            </p>
            <p>
              <CIcon icon={cilGroup} className="me-2 text-info" /> <strong>Following:</strong>{' '}
              {formatNumber(author.max_following_count)}
            </p>
            <p>
              <CIcon icon={cilLink} className="me-2" />{' '}
              <strong>
                Link:{' '}
                <a href={tiktokUrl} target="_blank" rel="noopener noreferrer">
                  Go to TikTok
                </a>
              </strong>
            </p>
          </div>
        ) : (
          <p>No author selected.</p>
        )}
      </COffcanvasBody>
    </COffcanvas>
  )
}

AuthorDetailsOffcanvas.propTypes = {
  visible: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  author: PropTypes.shape({
    nickname: PropTypes.string,
    signature: PropTypes.string,
    verified: PropTypes.bool,
    last_collected_at: PropTypes.string,
    max_follower_count: PropTypes.number,
    max_video_count: PropTypes.number,
    max_heart_count: PropTypes.number,
    max_following_count: PropTypes.number,
    unique_id: PropTypes.string,
  }),
}

export default AuthorDetailsOffcanvas
