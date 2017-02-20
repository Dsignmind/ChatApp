import * as React from 'react';

import { Socket } from './Socket';

const styles = {
    h1: { textAlign: 'center', fontFamily: 'Audiowide, cursive'},
    mainList: { float: 'right', width: '80%', height: '90%'},
    messageList: { float: 'right', width: '100%', overflow: 'scroll', height: '87%'},
    messageText: {fontFamily: 'Coming Soon, cursive', fontSize: '1.2em'},
    listStyle: { listStyleType: 'none' }
}

export class MessageList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            msgArr: [],
            messages: {'img': '', 'message_text': '', 'user': ''}
        };
    }

    componentDidMount() {
        var msgArr = this.state.msgArr;
        Socket.on('all messages', (data) => {
            this.setState({
                messages: {
                    'message_text': data['messages']['message_text'],
                    'user': data['messages']['user'], 
                    'img': data['messages']['img']
                }
            });
            msgArr.push(this.state.messages);
            this.forceUpdate();
        })

        
    }

    render() {
        let display_msgs = this.state.msgArr.map((msg, index) => 
            <li style={styles.messageText} key={index}>
                <span className="message-image"><img className="profile-img" src={msg.img} /></span>
                <span className="message-user">{msg.user}</span>
                <span className="message-text">{msg.message_text}</span>
            </li>
        );

        return (
            <div style={styles.mainList}>
                <div
                 className="fb-login-button"
                 data-max-rows="1"
                 data-size="medium"
                 data-show-faces="false"
                 data-auto-logout-link="true">
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
