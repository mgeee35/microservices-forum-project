
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import LoginPage from './LoginPage'
import SignUpPage from './SignUpPage'
import ForumPage from './ForumPage'

const App = () =>  {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage/>} />
        <Route path="/signup" element={<SignUpPage />} />
        <Route path="/forum" element={<ForumPage />} />
      </Routes>
    </Router>
  );
}

export default App