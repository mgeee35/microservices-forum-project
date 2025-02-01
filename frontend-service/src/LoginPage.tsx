import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom'; 
import {useState} from 'react';


const LoginPage = () => {
  
  const navigate = useNavigate();

  let followerData : String | null;
  let postsData : String | null;

  const loginEvents = async (event:React.FormEvent) => {

    event.preventDefault();
    try {
      // Get Follower Data
      const followerResponse = await fetch("https://439d-31-223-84-100.ngrok-free.app/Follow/followers/1", {
        method: "GET",
        headers: {
          "ngrok-skip-browser-warning": "true"
        }
      });
      followerData = await followerResponse.json();
      // Get All Posts
      const postsResponse = await fetch("https://5cad-212-253-197-38.ngrok-free.app/post/list", {
        method: "GET",
        headers: {
          "ngrok-skip-browser-warning": "true"
        }
      });
      postsData = await postsResponse.json();
 
    } catch (error) {
      console.error('Error fetching data:', error);
    }
 
    const usernameElement = document.getElementById('username') as HTMLInputElement;
    let username = "";
    if (usernameElement) {
      username = usernameElement.value;
    }
    navigate('/forum', { state: { username,followerData,postsData} });
  };

    return(
        <div className="login-container">
          <h2 className="form-title">Login Page</h2>
          <form className="login-form" onSubmit={loginEvents}>
            <div className="input-wrapper">
              <input type="text" id="username" placeholder="Username" className="input-field"
              required/>
            </div>
            <div className="input-wrapper">
              <input type="password" placeholder="Password" className="input-field" required />
            </div>
    
            <button className="login-button" onClick={loginEvents} type='submit'>Log In</button>
          </form>
          
          <p className="signup-prompt">
            Don&apos;t have an account? <Link to="/signup" className="signup-link">Sign up</Link>
          </p>
        </div>
      )
};

export default LoginPage;