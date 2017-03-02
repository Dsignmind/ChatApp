import * as React from 'react';

import { Socket } from './Socket';

const styles = {
    h1: { textAlign: 'center', fontFamily: 'Audiowide, cursive'},
    mainList: { float: 'right', width: '80%', height: '90%', backgroundImage: "url('../static/img/patter.png')"},
    messageList: { float: 'right', width: '100%', overflow: 'scroll', height: '87%'},
    messageText: {fontFamily: 'Coming Soon, cursive', fontSize: '1.2em'},
    listStyle: { listStyleType: 'none' }
}

export class MessageList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            msgArr: [],
            messages: {'img': '', 'message_text': '', 'user': ''},
            'connected': false
        };
    }

    componentDidMount() {
        Socket.on('new messages', (data) => {
            this.setState({
                msgArr: data['messages'],
            });
        });
        
        Socket.on('initial setup', (data) => {
            this.setState({
                msgArr: data['messages'],
            });
        });
        
    }
    imageRender(message){
        if(message.substr(0,7) == 'http://' || message.substr(0,8) == 'https://'){
            if(message.substr(message.length - 3) == 'jpg' || message.substr(message.length - 3) == 'png' || 
            message.substr(message.length - 3) == 'gif' || message.substr(message.length - 3) == 'bmp' || message.substr(message.length - 3) == 'tiff'){
                return <span className="message-text"><img src={message} /></span>
            }else{
                return <span className="message-text"><a href={message}>{message}</a></span>
            }
        }else{
                return <span className="message-text">{message}</span>
            }
        
    }

    render() {
        let display_msgs = this.state.msgArr.map((msg, index) => 
            <li style={styles.messageText} key={index}>
                <span className="message-image"><img className="profile-img" src={msg.img} /></span>
                <span className="message-user">{msg.user}</span>
                { this.imageRender(msg.message_text) }
            </li>
        );

        return (
            <div style={styles.mainList}>
                <div className="g-signin2" data-theme="dark"></div>

                 <div
                 className="fb-login-button"
                 data-max-rows="1"
                 data-size="medium"
                 data-show-faces="false"
                 data-auto-logout-link="true" >
                 </div>
                <h1 style={styles.h1}>Messages so far !</h1>
                <hr/>
                <div style={styles.messageList}>
                    <ul className="message-list" style={styles.listStyle}>{display_msgs}</ul>
                    
                </div>
            </div>
        );
    }
}
