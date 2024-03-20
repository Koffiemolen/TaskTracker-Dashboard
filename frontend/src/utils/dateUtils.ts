// src/utils/dateUtils.ts
export const formatDate = (value: string): string => {
  if (!value) {
    return '-'
  }

  const date = new Date(value)
  const defaultDate = new Date('1900-01-01T00:00:00')
  if (date.getTime() === defaultDate.getTime()) {
    return '-'
  }

  // Specify options for toLocaleString if needed
  const options: Intl.DateTimeFormatOptions = { hour12: false }
  return date.toLocaleString('nl-NL', options)
}
