document.addEventListener('DOMContentLoaded', ()=>{
  const chatForm = document.getElementById('chatForm')
  const leadForm = document.getElementById('leadForm')
  const messages = document.getElementById('messages')

  chatForm?.addEventListener('submit', async e=>{
    e.preventDefault()
    const text = document.getElementById('userInput').value
    appendMessage('You: '+text)
    const res = await fetch('/api/chat/', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({text})})
    const data = await res.json()
    appendMessage('Bot: '+(data.reply||JSON.stringify(data)))
  })

  leadForm?.addEventListener('submit', async e=>{
    e.preventDefault()
    const form = new FormData(leadForm)
    const payload = Object.fromEntries(form.entries())
    await fetch('/api/leads/', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)})
    alert('Lead submitted')
    leadForm.reset()
  })

  async function loadLeads(){
    const res = await fetch('/api/leads/')
    if(res.ok){
      const leads = await res.json()
      const el = document.getElementById('leads')
      if(el) el.innerHTML = '<pre>'+JSON.stringify(leads, null, 2)+'</pre>'
    }
  }
  if(document.getElementById('leads')) loadLeads()

  function appendMessage(t){
    const d = document.createElement('div'); d.textContent = t; messages.appendChild(d); messages.scrollTop = messages.scrollHeight
  }
})
