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
        // FB.getLoginStatus((response) => {
        //     if (response.status == 'unknown') {
        //         Socket.emit('del user', {
        //             'facebook_user_token': response.authResponse.accessToken
        //         });
        //         console.log("deleting user from userlist")
        //     }
        // });
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
