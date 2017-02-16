import * as React from 'react';

import { Socket } from './Socket';
import { MessageForm } from './MessageForm';
import { MessageList } from './MessageList';
import { UserList } from './UserList';



export class Content extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'numbers': []
        };
    }

    componentDidMount() {
        Socket.on('all numbers', (data) => {
            this.setState({
                'numbers': data['numbers']
            });
        })
    }

    render() {
        let numbers = this.state.numbers.map(
            (n, index) => <li key={index}>{n}</li>
        );
        return (
            <div>
                
                <UserList />
                <MessageList />
                <MessageForm />
            </div>
        );
    }
}
