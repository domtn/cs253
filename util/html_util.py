def escape_html(s):
  s = s.replace("&", "&amp;")
  s = s.replace(">", "&gt;")
  s = s.replace("<", "&lt;")
  s = s.replace("\"", "&quot;")
  
  return s