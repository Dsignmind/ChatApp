import * as React from 'react';
import { Socket } from './Socket';
import { MessageForm } from './MessageForm';
import { MessageList } from './MessageList';
import { UserList } from './UserList';
/*global FB*/


export class Content extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'usersArr': [],
            'userInfo': [],
            'connected' : false
        };
    }

    componentDidMount() {
        FB.Event.subscribe('auth.logout', Socket.emit('delete user'));
            
    }
    
    

    render() {
        return (
            <div>
                <UserList />
                <MessageList />
                <MessageForm />
                
            </div>
        );
    }
}
