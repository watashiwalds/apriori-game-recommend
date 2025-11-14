import { CButton } from '@coreui/react'

export const SelectedItem = ({ index, gameName, duration, dispatch }) => {
  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        background: '#f5f5f5',
        padding: '6px 10px',
        margin: '4px',
        borderRadius: '20px',
        fontSize: '0.9rem',
        color: '#333',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
      }}
    >
      <span style={{ fontWeight: 500 }}>{gameName}</span>

      {duration && (
        <span style={{ fontSize: '0.8rem', color: '#888', marginLeft: '6px' }}>({duration}h)</span>
      )}

      <CButton
        color="link"
        size="sm"
        style={{
          marginLeft: '8px',
          color: '#ff4d4f',
          fontWeight: 'bold',
          lineHeight: 1,
          padding: '0 6px',
          textDecoration: 'none',
        }}
        onClick={() => dispatch({ type: 'DELETE_SELECTED_GAME', payload: index })}
      >
        ×
      </CButton>
    </span>
  )
}
