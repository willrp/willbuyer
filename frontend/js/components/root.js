//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { BrowserRouter as Router } from "react-router-dom";
//IMPORT EXTERNAL FUNCTIONS=================================================
import { hot } from "react-hot-loader";

//IMPORT INTERNAL COMPONENTS================================================
import App from "components/app";

//IMPORT CONTEXTS===========================================================
import CartContextProvider from "contexts/cart-context";
import CurrentUserContextProvider from "contexts/current-user-context";
import SidebarContextProvider from "contexts/sidebar-context";

//COMPONENT=================================================================
function Root() {
    return (
        <Router>
            <CartContextProvider>
                <CurrentUserContextProvider>
                    <SidebarContextProvider>
                        <App />
                    </SidebarContextProvider>
                </CurrentUserContextProvider>
            </CartContextProvider>
        </Router>
    )
};

//EXPORT COMPONENT==========================================================
export default hot(module)(Root);