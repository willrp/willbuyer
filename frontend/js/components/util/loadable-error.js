//IMPORT EXTERNAL COMPONENTS================================================
import React, { Component } from "react";
import { Message, Icon } from "semantic-ui-react";

//IMPORT INTERNAL FUNCTIONS=================================================
import toastMessage from "lib/toast-message";

//COMPONENT=================================================================
class LoadableError extends Component {
    constructor(props) {
        super(props);
        this.state = { 
            hasError: false
        };
    }
  
    static getDerivedStateFromError(error) {
        if(error.status !== undefined && error.status === 601){
            toastMessage("error", { message: error.error, submessage: "Please refresh the page."})
        }

        return { 
            hasError: true
        };
    }
  
    // componentDidCatch(error, errorInfo) {
        // logErrorToMyService(error, errorInfo);
    // }
  
    render() {
        if (this.state.hasError) {
            return (
                <Message icon error>
                    <Icon name="exclamation triangle" />
                    <Message.Content>
                        <Message.Header>Error</Message.Header>
                        Something went wrong while displaying this webpage. To continue, please reload. 
                    </Message.Content>
                </Message>
            )
        }
        else{
            return this.props.children;
        }
    }
}

//EXPORT COMPONENT==========================================================
export default LoadableError;