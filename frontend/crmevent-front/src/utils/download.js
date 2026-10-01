export function downloadResponse(response, fallbackFilename) {
  const disposition = response.headers?.["content-disposition"] ?? ""
  const utfMatch = disposition.match(/filename\*=UTF-8''([^;]+)/i)
  const basicMatch = disposition.match(/filename="?([^";]+)"?/i)
  const filename = decodeURIComponent(utfMatch?.[1] ?? basicMatch?.[1] ?? fallbackFilename)
  const url = URL.createObjectURL(response.data)
  const link = document.createElement("a")
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  link.remove()
  URL.revokeObjectURL(url)
}
