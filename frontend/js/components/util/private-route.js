//IMPORT EXTERNAL COMPONENTS================================================
import React, { useContext } from "react";
import { Redirect, Route } from "react-router-dom";

//IMPORT CONTEXTS===========================================================
import { CurrentUserContext } from "contexts/current-user-context";

//COMPONENT=================================================================
function PrivateRoute({ component, ...rest }) {
    const { isLoggedIn } = useContext(CurrentUserContext);
    const Component = component;

    return (
        <Route
            {...rest}
            render={props =>
                (isLoggedIn) ? (
                    <Component {...props} />
                ) : (
                    <Redirect to={{ pathname: "/login", state: { from: props.location }}}/>
                )
            }
        />
    )
}

//EXPORT COMPONENT==========================================================
export default PrivateRoute;