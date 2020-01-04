//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { Header, Image, Icon } from "semantic-ui-react";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";
import { toast } from "react-toastify";

//STYLE CLASSES DEFINITION==================================================
const loginClass = css({
    "&&&&": {
        background: "lightskyblue",
        color: "black"
    },
    "&&&& .Toastify__close-button": {
        color: "black"
    }
});

const progressClass = css({
    "&&&&": {
        backgroundColor: "black"
    }
});


const headerClass = css({
    "&&&&, &&&& *": {
        color: "white"
    }
});

//AUX COMPONENTS============================================================
function Login({ name, picture }) {
    return (
        <Header as="h4" className={loginClass}>
            <Image src={picture} alt=" " />
                <Header.Content>
                    Welcome
                <Header.Subheader>{name}</Header.Subheader>
            </Header.Content>
        </Header>
    )
}

function Error({ message, submessage }) {
    return (
        <Header as="h4" className={headerClass}>
            <Icon name="warning sign" />
                <Header.Content>
                    {message}
                <Header.Subheader>{submessage}</Header.Subheader>
            </Header.Content>
        </Header>
    )
}

function Info({ message, submessage }) {
    return (
        <Header as="h4" className={headerClass}>
            <Icon name="info circle" />
                <Header.Content>
                    {message}
                <Header.Subheader>{submessage}</Header.Subheader>
            </Header.Content>
        </Header>
    )
}

//MAIN FUNCTION=============================================================
export default function toastMessage(type, props) {
    if(type === "error") {
        toast.error(<Error {...props} />, 
        {
            position: toast.POSITION.BOTTOM_RIGHT,
            closeOnClick: false,
            autoClose: false
        });
    }
    else if(type === "login") {
        toast.info(<Login {...props} />, {
            position: toast.POSITION.BOTTOM_RIGHT,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            autoClose: true,
            className: loginClass,
            progressClassName: progressClass,
            delay: 1000
        });
    }
    else{
        toast.info(<Info {...props} />, {
            position: toast.POSITION.BOTTOM_RIGHT,
            closeOnClick: true,
            autoClose: true
        });
    }
}