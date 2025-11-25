import {
  SET_FILTERED_GAME,
  ADD_SELECTED_GAME,
  DELETE_SELECTED_GAME,
  SET_SEARCH_TEXT,
  SET_DEBOUNCED_TEXT,
  SET_DURATION_TEXT,
  SET_DROPDOWN,
} from './gameSearchAction'

export const reducer = (state, action) => {
  switch (action.type) {
    case SET_FILTERED_GAME:
      return { ...state, filteredGames: action.payload }
    case ADD_SELECTED_GAME:
      return {
        ...state,
        selectedGames: [...state.selectedGames, action.payload],
      }
    case DELETE_SELECTED_GAME:
      const newGames = [...state.selectedGames]
      newGames.splice(action.payload, 1)
      return { ...state, selectedGames: newGames }
    case SET_SEARCH_TEXT:
      return { ...state, searchText: action.payload }
    case SET_DEBOUNCED_TEXT:
      return { ...state, debouncedText: action.payload }
    case SET_DURATION_TEXT:
      return { ...state, durationText: action.payload }
    case SET_DROPDOWN:
      return { ...state, showDropdown: action.payload }
    default:
      break
  }
}
