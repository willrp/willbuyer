//IMPORT EXTERNAL COMPONENTS================================================
import React, { Fragment, useContext } from "react";
import { Redirect } from "react-router-dom";
import { useLocation } from "react-router";
import { Header, Icon, Button } from "semantic-ui-react";

//IMPORT CONTEXTS===========================================================
import { CurrentUserContext } from "contexts/current-user-context";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const headerClass = css({
    "&&&&&": {
        marginTop: "0.5em"
    }
})

//COMPONENT=================================================================
function Login() {
    const { isLoggedIn } = useContext(CurrentUserContext);
    const { pathname, state } = useLocation();

    var redirVar = "?next=" + pathname;

    if(typeof state !== "undefined" && "from" in state){
        redirVar = "?next=" + state.from.pathname;
    }
    else if(pathname === "/login"){
        redirVar = "";
    }
    
    if(isLoggedIn){
        return <Redirect to="" />
    }
    else{
        return (
            <Fragment>
                <Header className={headerClass} as="h1" textAlign="center" dividing>
                    <Header.Content>
                        <Icon name="lock" />
                        Please log in
                        <Header.Subheader>To access restricted area</Header.Subheader>
                    </Header.Content>
                </Header>
                <Button
                    as="a"
                    href={"/auth/login" + redirVar}
                    color="blue"
                    fluid
                    size="massive"
                >
                    <Icon name="sign in" />
                    Log in
                </Button>
            </Fragment>
        )
    }
}

//EXPORT COMPONENT==========================================================
export default Login;