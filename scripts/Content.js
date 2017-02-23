import * as React from 'react';

import { Socket } from './Socket';
import { MessageForm } from './MessageForm';
import { MessageList } from './MessageList';
import { UserList } from './UserList';
import ReactDOM from 'react-dom';
import FacebookLogin from 'react-facebook-login';



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
        
    }
    
    
        
    
    

    render() {
        return (
            <div>
            
                
                <UserList />
                <MessageList array={this.state.msgArr}/>
                <MessageForm connected={this.state.connected}/>
                
            </div>
        );
    }
}
