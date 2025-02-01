import { useLocation } from 'react-router-dom';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const ForumPage = () => {

  const [userPostsData, setUserPostsData] = useState<any[]>([]);  // Post verisini tutmak için state
  const [userFollowerData, setUserFollowerData] = useState<any[]>([]);  // Follower verisini tutmak için state
  const location = useLocation();
  let { username, postsData, followerData } = location.state || {};  // location'dan veriyi alıyoruz
  const navigate = useNavigate();

  useEffect(() => {
    // postsData ve followerData verisi varsa, state'e set ediyoruz
    if (followerData) {
      setUserFollowerData(followerData.followerIds);
    }
    if (postsData) {
      setUserPostsData(postsData.data);
    }
    }, [postsData, followerData]);

  const afterEvents = async () => {
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

    const sendPost = () => {

        const url = 'https://5cad-212-253-197-38.ngrok-free.app/posts';  // Değiştirilecek URL

        const content = document.getElementById('postingArea') as HTMLInputElement;;
        let contentText;
        if(content){
            contentText = content.value;
        }

        let data = {
            "title": "Title",
            "content": contentText,
            "author": username
        };
        // fetch ile POST isteği
        fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),  // Veriyi JSON formatında gönderiyoruz
        })
          .then((response) => {
            if (response.ok) {
              return response.json();
            }
            throw new Error('Bir hata oluştu');
          })
          .then((responseData) => {
            console.log('Başarıyla gönderildi:', responseData);
            // İsteğin başarılı olduğunu kullanıcıya bildirebilirsiniz
          })
          .catch((error) => {
            console.error('Hata:', error);
            // Hata mesajını kullanıcıya gösterebilirsiniz
          });

          afterEvents();

    };

    const followUser = () => {
        const url = 'https://439d-31-223-84-100.ngrok-free.app/Follow';  // Değiştirilecek URL

        const content = document.getElementById('list-posts-input-field') as HTMLInputElement;;
        let contentText;
        if(content){
            contentText = content.value;
        }

        let data = {
            "userId": contentText
        };
        // fetch ile POST isteği
        fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),  // Veriyi JSON formatında gönderiyoruz
        })
          .then((response) => {
            if (response.ok) {
              return response.json();
            }
            throw new Error('Bir hata oluştu');
          })
          .then((responseData) => {
            console.log('Başarıyla gönderildi:', responseData);
            // İsteğin başarılı olduğunu kullanıcıya bildirebilirsiniz
          })
          .catch((error) => {
            console.error('Hata:', error);
            // Hata mesajını kullanıcıya gösterebilirsiniz
          });

          afterEvents();
    }

    const listPostsByUsername = () => {


        const content = document.getElementById('list-posts-input-field') as HTMLInputElement;;
        let contentText;
        if(content){
            contentText = content.value;
        }
        
        let url = '';

        if(contentText === ''){
            url = 'https://5cad-212-253-197-38.ngrok-free.app/post/list';
        }
        else{
            url = 'https://5cad-212-253-197-38.ngrok-free.app/post/get/'+ contentText ;
        }


        // fetch ile POST isteği
        fetch(url, {
          method: 'GET',
          headers: {
            "ngrok-skip-browser-warning": "true"
          }
        })
          .then((response) => {
            if (response.ok) {
              return response.json();
            }
            throw new Error('Bir hata oluştu');
          })
          .then((responseData) => {
            setUserPostsData(responseData.data)
            console.log('Başarıyla gönderildi:', responseData);
            // İsteğin başarılı olduğunu kullanıcıya bildirebilirsiniz
          })
          .catch((error) => {
            console.error('Hata:', error);
            // Hata mesajını kullanıcıya gösterebilirsiniz
          });

    };

    return(
        <div className="forum-container">
            <div className="forum-header-container">
                <div className="forum-header">Forum Page</div>
            </div>
            <div className="forum-body-container">
                <div className="forum-body">
                    <div className="customer-content">Merhaba {username} <br />Paylaşımını Yap!</div>
                    <div className="forum-content">
                        <textarea name="postingArea" id="postingArea" className='forum-posting-area' placeholder='Durum Paylaş!'></textarea>
                        <button className='forum-button' id='postButton' onClick={sendPost}>Paylaş</button>
                        <input className='list-posts-input-field' id='list-posts-input-field' type="text" placeholder='Username' />
                        <div className='username-action-buttons'>
                            <button className='list-posts-by-username-button' onClick={listPostsByUsername}>Paylaşım Listele</button>
                            <button className='follow-username-button' onClick={followUser}>Kullanıcıyı Takip Et</button>
                        </div>
                        <div className='postsArea'>
                            <div className='myPostsArea'>Takipçilerin <div><ul>  {userFollowerData.map((item) => (
                                                                    <li key={item}>{item}</li> ))}
          </ul></div></div>
                            <div className='allPostsArea'>Tüm Paylaşımlar<div><ul>  {userPostsData.map((item) => (
                                                                    <li key={item.id}>{item.content}</li> ))}
          </ul></div></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
      )
};

export default ForumPage;