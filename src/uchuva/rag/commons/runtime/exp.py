from lxml import html

text = '(function(i,s,o,g,r,a,m){i["googleanalyticsobject"]=r;i[r]=i[r]||function(){(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1new date();a=s.createelement(o),m=s.getelementsbytagname(o)[0];a.async=1;a.src=g;m.parentnode.insertbefore(a,m)})(window,document,"script","https://www.google-analytics.com/analytics.js","ga");ga("create", "ua-44877169-6", {"cookiedomain":"auto"});ga("set", "anonymizeip", true);ga("send", "pageview"); window.a2a_config=window.a2a_config||{};a2a_config.callbacks=[];a2a_config.overlays=[];a2a_config.templates={};a2a_config.onclick = 1; a2a_config.prioritize = ["facebook", "twitter", "whatsapp", "linkedin"]; a2a_config.num_services = 4; row convocatorias | innpulsa pasar al contenido principal menu registrarme'

# Parse the HTML
tree = html.fromstring(text)

# Remove all script tags (JavaScript code)
for element in tree.xpath("//script"):
    element.getparent().remove(element)

# Get the cleaned text without JavaScript code
clean_text = tree.text_content()

print(clean_text.strip())  # strip() to remove leading/trailing spaces
