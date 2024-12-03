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
                <span key={i} className="badge bg-light text-dark">
                  {tag}
                </span>
              ))}
            </div>
            <p>
              <strong>Author:</strong> {post.author_name}
            </p>
            <p>
              <strong>Description:</strong> {post.post_description}
            </p>
            <p>
              <CIcon icon={cilMediaPlay} className="me-2" />
              <strong>Views:</strong> {post.current_views.toLocaleString()}
            </p>
            <p>
              <CIcon icon={cilCalendar} className="me-2 text-muted" />
              <strong>Last Updated:</strong> {new Date(post.collected_at).toLocaleString()}
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
    post_description: PropTypes.string,
    current_views: PropTypes.number,
    collected_at: PropTypes.string,
    challenges: PropTypes.arrayOf(PropTypes.string),
  }),
}

export default PostTrendsDetailsOffcanvas
