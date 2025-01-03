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
  cilCommentBubble,
  cilShare,
  cilBookmark,
  cilLink,
  cilCalendar,
} from '@coreui/icons'

const PostDetailsOffcanvas = ({ visible, onClose, post }) => {
  const authorUniqueId = post?.author_unique_id || 'unknown-author' // Provide a fallback value
  const tiktokUrl = `https://www.tiktok.com/@${authorUniqueId}/video/${post?.id || 'unknown-id'}`

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
          <strong>Post Details</strong>
        </COffcanvasTitle>
        <CCloseButton className="text-reset" onClick={onClose} />
      </COffcanvasHeader>
      <COffcanvasBody>
        {post ? (
          <div>
            <p>
              <strong>Description:</strong> {post.description}
            </p>
            <p>
              <CIcon icon={cilCalendar} className="me-2 text-muted" />{' '}
              <strong>Creation Date:</strong> {post.created_at}
            </p>
            <p>
              <CIcon icon={cilCalendar} className="me-2 text-muted" />{' '}
              <strong>Last Collection Date:</strong> {post.last_collected_at}
            </p>
            <p>
              <CIcon icon={cilMediaPlay} className="me-2" /> <strong>Views:</strong>{' '}
              {formatNumber(post.max_play_count)}
            </p>
            <p>
              <CIcon icon={cilHeart} className="me-2 text-danger" /> <strong>Likes:</strong>{' '}
              {formatNumber(post.max_digg_count)}
            </p>
            <p>
              <CIcon icon={cilCommentBubble} className="me-2 text-primary" />{' '}
              <strong>Comments:</strong> {formatNumber(post.max_comment_count)}
            </p>
            <p>
              <CIcon icon={cilShare} className="me-2 text-success" /> <strong>Shares:</strong>{' '}
              {formatNumber(post.max_share_count)}
            </p>
            <p>
              <CIcon icon={cilBookmark} className="me-2 text-warning" /> <strong>Saves:</strong>{' '}
              {formatNumber(post.max_collect_count)}
            </p>
            <p>
              <CIcon icon={cilLink} className="me-2" />{' '}
              <strong>
                TikTok Video:{' '}
                <a href={tiktokUrl} target="_blank" rel="noopener noreferrer">
                  Watch here
                </a>
              </strong>
            </p>
          </div>
        ) : (
          <p>No post selected.</p>
        )}
      </COffcanvasBody>
    </COffcanvas>
  )
}

PostDetailsOffcanvas.propTypes = {
  visible: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
  post: PropTypes.shape({
    description: PropTypes.string,
    max_play_count: PropTypes.number,
    max_digg_count: PropTypes.number,
    max_comment_count: PropTypes.number,
    max_share_count: PropTypes.number,
    max_collect_count: PropTypes.number,
    author_unique_id: PropTypes.string,
    id: PropTypes.string,
    created_at: PropTypes.string,
    last_collected_at: PropTypes.string,
  }),
}

export default PostDetailsOffcanvas
