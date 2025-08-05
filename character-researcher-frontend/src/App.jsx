import './App.css'
import Research from './Research'
import Chat from './Chat'
import Compare from './Compare'

function App() {
  return (
    <main>
      <h1>Character Researcher</h1>
      <div style={{ display: "flex", gap: "2rem", flexWrap: "wrap" }}>
        <Research />
        <Chat />
        <Compare />
      </div>
      {/* Ready for backend API integration */}
    </main>
  )
}

export default App
