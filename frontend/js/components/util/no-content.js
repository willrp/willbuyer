//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { Message, Icon } from "semantic-ui-react";

//COMPONENT=================================================================
function NoContent({ message }) {
    return (
         <Message icon warning>
            <Icon name="warning sign" />
            <Message.Content>
                <Message.Header>No Results</Message.Header>
                {message}
            </Message.Content>
        </Message>
    )
}

//EXPORT COMPONENT==========================================================
export default NoContent;