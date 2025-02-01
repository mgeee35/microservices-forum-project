

const SignUpPage = () => {
    return(
        <div className="signup-container">
          <h2 className="signup-title">Sign Up</h2>
          <form action="#" className="signup-form">
            <div className="input-wrapper">
              <input type="email" placeholder="Email address" className="input-field"
              required/>
            </div>
            <div className="input-wrapper">
              <input type="text" placeholder="Username" className="input-field"
              required/>
            </div>
            <div className="input-wrapper">
              <input type="password" placeholder="Password" className="input-field" required />
            </div>
    
            <button className="signup-button">Sign In</button>
          </form>
          
        </div>
      )
};

export default SignUpPage;