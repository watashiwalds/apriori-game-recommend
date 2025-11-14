import { createContext, useContext, useState } from 'react'

const AppContext = createContext()

export const AppProvider = ({ children }) => {
  const [data, setData] = useState({}) // lưu key:value

  const updateData = (key, value) => {
    setData((prev) => ({ ...prev, [key]: value }))
  }

  return <AppContext.Provider value={{ data, updateData }}>{children}</AppContext.Provider>
}

export const useAppContext = () => useContext(AppContext)
