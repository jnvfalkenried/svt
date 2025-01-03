import React from 'react'
import { CCard, CCardHeader, CCardBody } from '@coreui/react'
import RelatedHashtags from './RelatedHashtags'

const HashtagAssociations = () => {
  return (
    <>
      <CCard className="mb-4">
        <CCardHeader>Hashtag Associations</CCardHeader>
        <CCardBody>
          <RelatedHashtags />
        </CCardBody>
      </CCard>
    </>
  )
}

export default HashtagAssociations
