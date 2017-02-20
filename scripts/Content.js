import * as React from 'react';

import { Socket } from './Socket';
import { MessageForm } from './MessageForm';
import { MessageList } from './MessageList';
import { UserList } from './UserList';



export class Content extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'msgArr': [],
            'userInfo': [],
            'connected' : false
        };
    }

    componentDidMount() {
        FB.getLoginStatus((response) => {
            if (response.status == 'connected' && this.state.connected == false) {
                console.log('Initializing connection: ');
                Socket.emit('initial connect', {
                    'facebook_user_token': response.authResponse.accessToken,
                });
                console.log('Sent authentication token to server!');
                this.setState({connected:true});
                this.forceUpdate();
            }
        });
        Socket.on('initial setup', (data) => {
            this.setState({
                msgArr: data['messages'],
                userInfo: data['userInfo']
                
            });
            //console.log(this.state.userInfo['user']);
            this.forceUpdate();
        })
        
    }
    

    render() {
        return (
            <div>
                
                <UserList />
                <MessageList array={this.state.msgArr}/>
                <MessageForm />
                
            </div>
        );
    }
}
