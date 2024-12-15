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
import { cilMediaPlay, cilLink, cilCalendar } from '@coreui/icons'

const PostTrendsDetailsOffcanvas = ({ visible, onClose, post }) => {
  const tiktokUrl = `https://www.tiktok.com/@${post?.author_name}/video/${post?.post_id}`
  return (
    <COffcanvas placement="end" visible={visible} onHide={onClose} style={{ width: '30%' }}>
      <COffcanvasHeader>
        <COffcanvasTitle>
          <strong>Post Details</strong>
        </COffcanvasTitle>
        <CCloseButton className="text-reset" onClick={onClose} />
      </COffcanvasHeader>
      <COffcanvasBody>
        {post ? (
          <div>
            <div className="d-flex flex-wrap gap-2 mb-3">
              {post.challenges.map((tag, i) => (
                <span key={i} className="badge bg-body-tertiary text-medium-emphasis">
                  {tag}
                </span>
              ))}
            </div>
            <p>
              <strong>Current Views:</strong> {post.current_views?.toLocaleString()}
            </p>
            <p>
              <strong>Daily Change:</strong> {post.daily_change?.toLocaleString()}
            </p>
            <p>
              <strong>Weekly Change:</strong> {post.weekly_change?.toLocaleString()}
            </p>
            <p>
              <strong>Monthly Change:</strong> {post.monthly_change?.toLocaleString()}
            </p>
            <p>
              <CIcon icon={cilCalendar} className="me-2 text-muted" />
              <strong>Last Updated:</strong>{' '}
              {new Date(post.collected_at).toLocaleString()}
            </p>
            <p>
              <CIcon icon={cilLink} className="me-2" />
              <a href={tiktokUrl} target="_blank" rel="noopener noreferrer">
                Watch on TikTok
              </a>
            </p>
          </div>
        ) : (
          <p>No post selected.</p>
        )}
      </COffcanvasBody>
    </COffcanvas>
  )
}

PostTrendsDetailsOffcanvas.propTypes = {
  visible: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  post: PropTypes.shape({
    post_id: PropTypes.string,
    author_name: PropTypes.string,
    current_views: PropTypes.number,
    daily_change: PropTypes.number,
    weekly_change: PropTypes.number,
    monthly_change: PropTypes.number,
    collected_at: PropTypes.string,
    challenges: PropTypes.arrayOf(PropTypes.string),
  }),
}

export default PostTrendsDetailsOffcanvas