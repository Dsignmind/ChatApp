// JavaScript Fileimport * as React from 'react';
import * as React from 'react';
import { Socket } from './Socket';
/*global FB*/

const styles = {
    formBody: {  background: '#000', padding: '3px', position: 'fixed', bottom:'0' , width: '100%'},
    formInput: { border: '0', padding: '10px', width: '90%', marginRight: '.5%' },
    formButton: { width: '9%', background: 'rgb(130, 224, 255)', border: 'none', padding: '10px'}
}

export class MessageForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'message_info' : [],
            'img': '',
            'user': '',
            'message_text': '',
            'buttonText': "Get History",
            'connected': false
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    
    handleChange(event) {
        this.setState({message_text: event.target.value});
    }
    
    handleSubmit(event) {
        event.preventDefault();
        FB.getLoginStatus((response) => {
            if (response.status == 'connected') {
                if(this.state.connected == true) {
                    var {message_info} = this.state;
                    message_info.push({
                        img: this.state.img, user: this.state.user, message_text: this.state.message_text
                    });
                    
                    console.log('Generated a message: ', this.state.message_info);
                    Socket.emit('new message', {
                        'facebook_user_token': response.authResponse.accessToken,
                        'message': message_info
                    });
                    console.log('Sent up the message to server!');
                    this.setState({message_text: '', message_info: []});
                    this.forceUpdate();
                } else {
                    console.log('Initializing connection: ');
                    Socket.emit('initial connect');
                    console.log('Sent authentication token to server!');
                    Socket.emit('new user', {
                        'facebook_user_token': response.authResponse.accessToken
                    });
                    console.log("sending new user to server");
                    this.setState({connected: true, buttonText: "Submit"});
                }
             } //else {
            //     let auth = gapi.auth2.getAuthInstance();
            //     let user = auth.currentUser.get();
            //     if(user.isSignedIn()) {
            //         console.log('Generated a message: ', this.state.message_info);
            //         Socket.emit('new message', {
            //         'google_user_token': user.getAuthResponse().id_token,
            //         'facebook_user_token': '',
            //         'message': message_info,
            //     });
            //     console.log('Sent up the message to server!');
            //     this.setState({message_text: '', message_info: []});
            //     this.forceUpdate();
            //     }
            // }
        });
    
}



    

    render() {
        return (
            <div>
                <form style={styles.formBody} onSubmit={this.handleSubmit}>
                    <label>
                        <input id="messagebox"
                            style={styles.formInput}
                            placeholder="Enter message..."
                            value={this.state.message_text}
                            onChange={this.handleChange}
                            />
                        <script>document.getElementById("messagebox").select();</script>
                    </label>
                    <input style={styles.formButton} type="submit" value={this.state.buttonText} />
                </form>
            </div>
        );
    }
}
