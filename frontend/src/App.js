import './App.css'
import { CContainer } from '@coreui/react'
import '@coreui/coreui/dist/css/coreui.min.css'
import GameSearch from './components/GameSearch'
import { AppProvider } from './components/AppContext'

function App() {
  return (
    <AppProvider>
      <CContainer style={{ marginTop: 16, padding: 0 }}>
        <GameSearch />
      </CContainer>
    </AppProvider>
  )
}

export default App
