import * as React from 'react';

import { Socket } from './Socket';

const styles = {
    h1: { textAlign: 'center', fontFamily: 'Audiowide, cursive'},
    userList: { float: 'left', background: 'rgb(220, 223, 224)', width: '20%', height: '90%', borderRadius: '10px'},
    userText: {fontFamily: 'Khand, sans-serif', fontSize: '1.2em'},
    listStyle: { listStyleType: 'square' }
}

export class UserList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'users': ['Chat-Bot']
        };
    }

    componentDidMount() {
        Socket.on('all users', (data) => {
            this.setState({
                'users': data['users']
            });
        })
    }

    render() {
        let users = this.state.users.map(
            (usr, index) => <li style={styles.userText} key={index}>{usr}</li>
        );
        return (
            <div style={styles.userList}>
                <h1 style={styles.h1} >Users online</h1>
                <hr/>
                <ul style={styles.listStyle}>{users}</ul>
            </div>
        );
    }
}
