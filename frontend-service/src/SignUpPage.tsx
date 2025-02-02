import { useState } from "react";
const SignUpPage = () => {
    const [formData, setFormData] = useState({
        username: "",
        password: "",
        emailaddress: ""
    });
    const handleChange = (e: { target: { name: any; value: any; }; }) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };
    const handleSubmit = async (e: { preventDefault: () => void; }) => {
        e.preventDefault();
        try {
            const response = await fetch("https://mosquito-dear-mainly.ngrok-free.app/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            });
            const data = await response.json();
            console.log("Response:", response.status, data);
            if (response.ok) {
                // Kayıt başarılıysa Google'a yönlendir
                alert("Kullanıcı başarıyla kaydedildi!");
                window.location.href = "http://localhost:5173/";
            } else if (response.status === 409) {
                alert("Bu kullanıcı adı veya e-posta zaten kayıtlı!");
            } else {
                alert("Kayıt başarısız oldu, lütfen tekrar deneyin.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Bir hata oluştu, lütfen tekrar deneyin.");
        }
    };
    return (
        <div className="signup-container">
            <h2 className="signup-title">Sign Up</h2>
            <form onSubmit={handleSubmit} className="signup-form">
                <div className="input-wrapper">
                    <input
                        type="text"
                        name="username"
                        placeholder="Username"
                        className="input-field"
                        required
                        value={formData.username}
                        onChange={handleChange}
                    />
                </div>
                <div className="input-wrapper">
                    <input
                        type="password"
                        name="password"
                        placeholder="Password"
                        className="input-field"
                        required
                        value={formData.password}
                        onChange={handleChange}
                    />
                </div>
                <div className="input-wrapper">
                    <input
                        type="email"
                        name="emailaddress"
                        placeholder="Email address"
                        className="input-field"
                        required
                        value={formData.emailaddress}
                        onChange={handleChange}
                    />
                </div>
                <button type="submit" className="signup-button">Sign Up</button>
            </form>
        </div>
    );
};
export default SignUpPage;