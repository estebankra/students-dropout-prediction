import { shallowRef } from 'vue'

const headerContent = shallowRef({ content: '' })

export function useHeaderContent() {
  const setHeaderContent = (newContent) => {
    headerContent.value = { content: newContent }
  }
  return { headerContent, setHeaderContent }
}
