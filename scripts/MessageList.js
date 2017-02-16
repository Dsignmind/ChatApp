import * as React from 'react';

import { Button } from './Button';
import { Socket } from './Socket';

const styles = {
    h1: { textAlign: 'center', fontFamily: 'Audiowide, cursive'},
    mainList: { float: 'right', width: '80%', height: '90%'},
    messageList: { float: 'right', width: '100%', overflow: 'scroll', height: '87%'},
    messageText: {fontFamily: 'Coming Soon, cursive', fontSize: '1.2em'},
    listStyle: { listStyleType: 'square' }
}

export class MessageList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'messages': []
        };
    }

    componentDidMount() {
        Socket.on('all messages', (data) => {
            this.setState({
                'messages': data['messages']
            });
        })
    }

    render() {
        let messages = this.state.messages.map(
            (msg, index) => <li style={styles.messageText} key={index}>{msg}</li>
        );
        return (
            <div style={styles.mainList}>
                <h1 style={styles.h1}>Messages so far !</h1>
                <hr/>
                <div style={styles.messageList}>
                    <ul style={styles.listStyle}>{messages}</ul>
                </div>
            </div>
        );
    }
}
