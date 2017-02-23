import * as React from 'react';

import { Socket } from './Socket';

const styles = {
    h1: { textAlign: 'center', fontFamily: 'Audiowide, cursive'},
    userList: { float: 'left', background: 'rgb(220, 223, 224)', width: '20%', height: '90%', borderRadius: '10px'},
    userText: {fontFamily: 'Khand, sans-serif', fontSize: '1.2em'},
    listStyle: { listStyleType: 'none' }
}

export class UserList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'usersArr': []
        };
    }

    componentDidMount() {
        Socket.on('all users', (data) => {
            this.setState({
                usersArr: data['users'],
            });
            console.log(data['user']);
        });
    }

    render() {
        let display_users = this.state.usersArr.map((usr, index) => 
        <li style={styles.userText} key={index}>
            <span className="message-image"><img className="profile-img" src={usr.img} /></span>
            <span className="message-user">{usr.user}</span></li>
        );
        return (
            <div style={styles.userList}>
                <h1 style={styles.h1} >Users online</h1>
                <hr/>
                <ul style={styles.listStyle}>{display_users}</ul>
            </div>
        );
    }
}
