// JavaScript Fileimport * as React from 'react';
import * as React from 'react';

import { Socket } from './Socket';

const styles = {
    formBody: {  background: '#000', padding: '3px', position: 'fixed', bottom:'0' , width: '100%'},
    formInput: { border: '0', padding: '10px', width: '90%', marginRight: '.5%' },
    formButton: { width: '9%', background: 'rgb(130, 224, 255)', border: 'none', padding: '10px'}
}

export class MessageForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'message_text': ''};
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    
    handleChange(event) {
        this.setState({message_text: event.target.value});
    }
    
    handleSubmit(event) {
        event.preventDefault();
        console.log('Generated a message: ', this.state.message_text);
        Socket.emit('new message', {
            'message': this.state.message_text,
        });
        console.log('Sent up the message to server!');
        this.setState({message_text: ''});
    }

    render() {
        return (
            <div>
                <form style={styles.formBody} onSubmit={this.handleSubmit}>
                    <label>
                        <input style={styles.formInput}
                            placeholder="Enter message..."
                            value={this.state.message_text}
                            onChange={this.handleChange}
                            />
                    </label>
                    <input style={styles.formButton} type="submit" value="Submit" />
                </form>
            </div>
        );
    }
}
