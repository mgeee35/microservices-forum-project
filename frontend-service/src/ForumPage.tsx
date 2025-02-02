import { useLocation } from 'react-router-dom';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
const ForumPage = () => {
  const [userPostsData, setUserPostsData] = useState<any[]>([]);  // Post verisini tutmak için state
  const [userFollowerData, setUserFollowerData] = useState<any[]>([]);  // Follower verisini tutmak için state
  const location = useLocation();
  let { username, postsData, followerData,userInfoID } = location.state || {};  // location'dan veriyi alıyoruz
  const navigate = useNavigate();
  useEffect(() => {
    // postsData ve followerData verisi varsa, state'e set ediyoruz
    if (followerData) {
      setUserFollowerData(followerData.usernames);
    }
    if (postsData) {
      setUserPostsData(postsData.data);
    }
    }, [postsData, followerData]);
  const afterEvents = async () => {
    try {
      // Get Follower Data
      const followerResponse = await fetch("https://fly-next-shrimp.ngrok-free.app/Follow/followers/" + userInfoID, {
        method: "GET",
        headers: {
          "ngrok-skip-browser-warning": "true"
        }
      });
      followerData = await followerResponse.json();
      // Get All Posts
      const postsResponse = await fetch("https://relaxing-humble-snapper.ngrok-free.app/post/list", {
        method: "GET",
        headers: {
          "ngrok-skip-browser-warning": "true"
        }
      });
      postsData = await postsResponse.json();
    } catch (error) {
      console.error('Error fetching data:', error);
    }
    navigate('/forum', { state: { username,followerData,postsData,userInfoID} });
  };
    const sendPost = () => {
        const url = 'https://relaxing-humble-snapper.ngrok-free.app/post/create';  // Değiştirilecek URL
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
            alert('Post başarıyla atıldı.')
            // İsteğin başarılı olduğunu kullanıcıya bildirebilirsiniz
          })
          .catch((error) => {
            console.error('Hata:', error);
            alert('Post servisi hata aldı.')
            // Hata mesajını kullanıcıya gösterebilirsiniz
          });
          afterEvents();
    };
    const followUser = () => {



        //const url = 'https://fly-next-shrimp.ngrok-free.app/Follow';  // Değiştirilecek URL
        const url = "https://mosquito-dear-mainly.ngrok-free.app/getUserID";
        const content = document.getElementById('list-posts-input-field') as HTMLInputElement;;
        let contentText;
        if(content){
            contentText = content.value;
        }
        let data = {
            "username": contentText
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
            if(responseData.userID===undefined || responseData.userID===null){
              alert('Böyle bir kullanıcı bulunmamaktadır.');
              return;
            }
            console.log('Başarıyla gönderildi:', responseData);
            const url = 'https://fly-next-shrimp.ngrok-free.app/Follow';
            let data = {
              "userId": userInfoID,
              "followerId" : responseData.userID.id
            };
            fetch(url, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(data),  // Veriyi JSON formatında gönderiyoruz
            })
            .then((response) => {
              if (response.ok) {
                alert('Takip edilmeye başlandı.')
              }
              else{
                alert('Kullanıcı zaten takip ediliyor.')
              }
            })
            .then((responseData) => {
              console.log('Başarıyla gönderildi:', responseData);
              afterEvents();
            })
          })
          .catch((error) => {
            console.error('Hata:', error);
            // Hata mesajını kullanıcıya gösterebilirsiniz
          });
    }
    const listPostsByUsername = () => {
        const content = document.getElementById('list-posts-input-field') as HTMLInputElement;;
        let contentText;
        if(content){
            contentText = content.value;
        }
        let url = '';
        if(contentText === ''){
            url = 'https://relaxing-humble-snapper.ngrok-free.app/post/list';
        }
        else{
            url = 'https://relaxing-humble-snapper.ngrok-free.app/post/get/'+ contentText ;
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